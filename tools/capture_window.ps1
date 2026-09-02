<#
.SYNOPSIS
  Capture the Obsidian window to a PNG.

.DESCRIPTION
  Obsidian's CLI has a dev:screenshot command, but on Windows it exits 127
  without a message, so the window is grabbed from the desktop instead:
  DwmGetWindowAttribute(9) for the true frame bounds -- GetWindowRect includes
  the invisible resize border -- and CopyFromScreen for the pixels. The window
  has to be on top and unobscured, hence the topmost/foreground dance.

  Foreground is not cosmetic here. Obsidian does not build the reading view
  while its window is in the background, so a script that only makes the window
  *visible* finds an empty pane. Windows refuses SetForegroundWindow to a
  process that does not already own the foreground, so the call is wrapped in
  AttachThreadInput against the current foreground thread, which is the
  documented way round the lock.

  Sizes are given in logical pixels; the PNG comes out at the display's scale
  factor, so on a 150% display -Width 1600 yields a 2400px-wide image.

.EXAMPLE
  pwsh tools/capture_window.ps1 -Out shot.png -Width 1600 -Height 900
#>
param(
  [Parameter(Mandatory = $true)][string]$Out,
  [int]$Width = 0,
  [int]$Height = 0,
  [int]$SettleMs = 900
)

Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;using System.Runtime.InteropServices;
public class WinCap {
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")] public static extern bool BringWindowToTop(IntPtr h);
 [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h,int c);
 [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
 [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h,IntPtr pid);
 [DllImport("user32.dll")] public static extern bool AttachThreadInput(uint a,uint b,bool attach);
 [DllImport("kernel32.dll")] public static extern uint GetCurrentThreadId();
 public static void Focus(IntPtr h) {
   uint fg = GetWindowThreadProcessId(GetForegroundWindow(), IntPtr.Zero);
   uint me = GetCurrentThreadId();
   bool attached = fg != me && AttachThreadInput(fg, me, true);
   BringWindowToTop(h);
   SetForegroundWindow(h);
   if (attached) AttachThreadInput(fg, me, false);
 }
 [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h,IntPtr a,int x,int y,int w,int ht,uint f);
 [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr h,int x,int y,int w,int ht,bool r);
 [DllImport("dwmapi.dll")] public static extern int DwmGetWindowAttribute(IntPtr h,int a,out RECT r,int s);
 [StructLayout(LayoutKind.Sequential)] public struct RECT{public int L,T,R,B;}
}
"@

$proc = Get-Process obsidian -ErrorAction SilentlyContinue |
        Where-Object { $_.MainWindowTitle -like "*Obsidian*" } | Select-Object -First 1
if (-not $proc) { throw "no Obsidian window found" }
$h = $proc.MainWindowHandle

[WinCap]::ShowWindow($h, 9) | Out-Null          # SW_RESTORE, in case it is maximised
if ($Width -gt 0 -and $Height -gt 0) {
  [WinCap]::MoveWindow($h, 40, 30, $Width, $Height, $true) | Out-Null
  Start-Sleep -Milliseconds 400
}
[WinCap]::SetWindowPos($h, [IntPtr](-1), 0,0,0,0, 0x0003) | Out-Null   # HWND_TOPMOST, no move/size

# Even with the thread-input trick the handover is occasionally refused, so
# retry, and fall back to a minimise/restore cycle -- which Windows always
# honours -- before giving up. SW_RESTORE puts the window back at the same
# rect, so the size set above survives.
$focused = $false
for ($i = 0; $i -lt 6 -and -not $focused; $i++) {
  [WinCap]::Focus($h)
  Start-Sleep -Milliseconds (150 * ($i + 1))
  $focused = ([WinCap]::GetForegroundWindow() -eq $h)
  if (-not $focused -and $i -eq 3) {
    [WinCap]::ShowWindow($h, 6) | Out-Null      # SW_MINIMIZE
    Start-Sleep -Milliseconds 250
    [WinCap]::ShowWindow($h, 9) | Out-Null      # SW_RESTORE
  }
}
if (-not $focused) {
  throw "could not bring the Obsidian window to the foreground -- it will not render in the background, so the grab would be of a blank pane"
}
Start-Sleep -Milliseconds $SettleMs

$r = New-Object WinCap+RECT
if ([WinCap]::DwmGetWindowAttribute($h, 9, [ref]$r, 16) -ne 0) { throw "DwmGetWindowAttribute failed" }
$w = $r.R - $r.L; $ht = $r.B - $r.T
if ($w -le 0 -or $ht -le 0 -or $ht -gt 20000) { throw "implausible window rect ${w}x${ht}" }

$bmp = New-Object System.Drawing.Bitmap $w, $ht
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($r.L, $r.T, 0, 0, $bmp.Size)
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()

[WinCap]::SetWindowPos($h, [IntPtr](-2), 0,0,0,0, 0x0003) | Out-Null   # HWND_NOTOPMOST
"${w}x${ht} -> $Out"
