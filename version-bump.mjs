/**
 * Records a release in versions.json, which tells older Obsidian installs the
 * newest version of the theme they are allowed to download.
 *
 * Usage: `npm version <patch|minor|major>`
 *
 * npm bumps package.json, then runs this to mirror the new version into
 * manifest.json and add a versions.json entry pointing at the current
 * minAppVersion.
 */

import { readFileSync, writeFileSync } from "fs";

const targetVersion = process.env.npm_package_version;

if (!targetVersion) {
	console.error(
		"npm_package_version is not set. Run this through `npm version <patch|minor|major>`, not directly."
	);
	process.exit(1);
}

const manifest = JSON.parse(readFileSync("manifest.json", "utf8"));
const { minAppVersion } = manifest;
manifest.version = targetVersion;
writeFileSync("manifest.json", JSON.stringify(manifest, null, 2) + "\n");

const versions = JSON.parse(readFileSync("versions.json", "utf8"));
versions[targetVersion] = minAppVersion;
writeFileSync("versions.json", JSON.stringify(versions, null, 2) + "\n");

console.log(`version ${targetVersion} (minAppVersion ${minAppVersion})`);
