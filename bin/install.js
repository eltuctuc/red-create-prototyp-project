#!/usr/bin/env node

import { createInterface } from 'readline';
import { cp, mkdir, rm, access } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { homedir } from 'os';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PACKAGE_ROOT = join(__dirname, '..');

// ─── Helpers ────────────────────────────────────────────────────────────────

const c = {
  red:    (s) => `\x1b[31m${s}\x1b[0m`,
  yellow: (s) => `\x1b[33m${s}\x1b[0m`,
  green:  (s) => `\x1b[32m${s}\x1b[0m`,
  cyan:   (s) => `\x1b[36m${s}\x1b[0m`,
  bold:   (s) => `\x1b[1m${s}\x1b[0m`,
  dim:    (s) => `\x1b[2m${s}\x1b[0m`,
};

const AGENT_FILES = [
  'frontend-developer.md',
  'backend-developer.md',
  'qa-engineer.md',
  'ux-reviewer.md',
];

// Sentinel file to detect an existing installation
const SENTINEL = join('commands', 'red-proto', 'create.md');

async function exists(path) {
  try { await access(path); return true; }
  catch { return false; }
}

function ask(rl, question) {
  return new Promise(resolve => rl.question(question, resolve));
}

function printHeader(version) {
  console.log('');
  console.log(c.red('  ██████╗ ███████╗██████╗ '));
  console.log(c.red('  ██╔══██╗██╔════╝██╔══██╗'));
  console.log(c.red('  ██████╔╝█████╗  ██║  ██║'));
  console.log(c.red('  ██╔══██╗██╔══╝  ██║  ██║'));
  console.log(c.red('  ██║  ██║███████╗██████╔╝'));
  console.log(c.red('  ╚═╝  ╚═╝╚══════╝╚═════╝ ') + c.dim(`· proto  v${version}`));
  console.log('');
  console.log(c.bold('  AI-powered product development framework'));
  console.log(c.dim('  for Claude Code – from idea to tested prototype'));
  console.log('');
  console.log('  ' + c.dim('─'.repeat(48)));
  console.log('');
}

// ─── Uninstall ───────────────────────────────────────────────────────────────

async function runUninstall() {
  const { version } = JSON.parse(
    await import('fs').then(fs => fs.promises.readFile(join(PACKAGE_ROOT, 'package.json'), 'utf8'))
  );

  printHeader(version);

  const rl = createInterface({ input: process.stdin, output: process.stdout });

  console.log(c.yellow('  Uninstall – where was red · proto installed?'));
  console.log('');

  const globalBase = join(homedir(), '.claude');
  const localBase  = join(process.cwd(), '.claude');

  const globalExists = await exists(join(globalBase, SENTINEL));
  const localExists  = await exists(join(localBase,  SENTINEL));

  if (!globalExists && !localExists) {
    console.log(c.dim('  red · proto is not installed in this location.'));
    console.log('');
    rl.close();
    return;
  }

  const options = [];
  if (globalExists) options.push({ label: `Global  ${c.dim('(~/.claude)')}`,  base: globalBase });
  if (localExists)  options.push({ label: `Local   ${c.dim('(./.claude)')}`,   base: localBase  });

  options.forEach((opt, i) => {
    console.log(`  ${i + 1}) ${c.bold(opt.label)}`);
  });
  if (options.length > 1) {
    console.log(`  ${options.length + 1}) ${c.bold('Both')}`);
  }
  console.log('');

  const max = options.length > 1 ? options.length + 1 : options.length;
  let choice = '';
  while (!Array.from({ length: max }, (_, i) => String(i + 1)).includes(choice)) {
    choice = (await ask(rl, c.dim('  Choice [1]: '))).trim() || '1';
  }

  const targets =
    options.length > 1 && choice === String(options.length + 1)
      ? options
      : [options[parseInt(choice) - 1]];

  console.log('');
  console.log(c.yellow('  ⚠  This will remove all red-proto commands and agents.'));
  console.log(c.dim('  Your project files (features/, research/, prd.md, …) are NOT touched.'));
  console.log('');

  const confirm = (await ask(rl, c.dim('  Type "yes" to confirm: '))).trim().toLowerCase();
  rl.close();

  if (confirm !== 'yes') {
    console.log('');
    console.log(c.dim('  Aborted. Nothing changed.'));
    console.log('');
    return;
  }

  let removed = 0;
  for (const target of targets) {
    const commandsDir = join(target.base, 'commands', 'red-proto');
    if (await exists(commandsDir)) {
      await rm(commandsDir, { recursive: true, force: true });
      removed++;
    }
    for (const file of AGENT_FILES) {
      const path = join(target.base, 'agents', file);
      if (await exists(path)) { await rm(path); removed++; }
    }
  }

  console.log('');
  console.log(c.green(`  ✓ Removed`));
  console.log(c.dim('  red · proto has been uninstalled.'));
  console.log('');
}

// ─── Install ─────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);

  if (args.includes('--uninstall') || args.includes('-u')) {
    return runUninstall();
  }

  const { version } = JSON.parse(
    await import('fs').then(fs => fs.promises.readFile(join(PACKAGE_ROOT, 'package.json'), 'utf8'))
  );

  printHeader(version);

  const rl = createInterface({ input: process.stdin, output: process.stdout });

  // ── Step 1: Install location ───────────────────────────────────────────────
  console.log(c.yellow('  Where would you like to install?'));
  console.log('');
  console.log(`  1) ${c.bold('Global')}  ${c.dim(`(~/.claude)`)}  – available in all your projects`);
  console.log(`  2) ${c.bold('Local')}   ${c.dim(`(./.claude)`)}  – this project only`);
  console.log('');

  let locationChoice = '';
  while (!['1', '2'].includes(locationChoice)) {
    locationChoice = (await ask(rl, c.dim('  Choice [1]: '))).trim() || '1';
    if (!['1', '2'].includes(locationChoice)) {
      console.log(c.red('  → Please enter 1 or 2'));
    }
  }

  const isGlobal = locationChoice === '1';
  const claudeBase = isGlobal ? join(homedir(), '.claude') : join(process.cwd(), '.claude');
  const label = isGlobal ? `~/.claude` : `./.claude`;

  // ── Duplicate detection ────────────────────────────────────────────────────
  const globalBase = join(homedir(), '.claude');
  const localBase  = join(process.cwd(), '.claude');
  const otherBase  = isGlobal ? localBase : globalBase;
  const otherLabel = isGlobal ? './.claude' : '~/.claude';

  const otherInstalled = await exists(join(otherBase, SENTINEL));
  if (otherInstalled) {
    console.log('');
    console.log(c.yellow(`  ⚠  red · proto is already installed in ${otherLabel}`));
    console.log(c.dim(`  Installing in both locations will show every command twice in Claude Code.`));
    console.log('');
    const proceed = (await ask(rl, c.dim('  Continue anyway? [y/N]: '))).trim().toLowerCase();
    if (proceed !== 'y') {
      console.log('');
      console.log(c.dim('  Aborted. Nothing changed.'));
      console.log('');
      rl.close();
      return;
    }
  }

  console.log('');

  // ── Step 2: Confirm if already installed ──────────────────────────────────
  const alreadyInstalled = await exists(join(claudeBase, SENTINEL));

  if (alreadyInstalled) {
    console.log(c.yellow(`  ⚠  red · proto is already installed in ${label}`));
    console.log('');
    console.log(`  1) ${c.bold('Add missing files only')}   ${c.dim('– safe, keeps existing customizations')}`);
    console.log(`  2) ${c.bold('Update to latest version')}  ${c.dim('– overwrites commands & agents, keeps project data')}`);
    console.log(`  3) ${c.bold('Cancel')}`);
    console.log('');

    let updateChoice = '';
    while (!['1', '2', '3'].includes(updateChoice)) {
      updateChoice = (await ask(rl, c.dim('  Choice [1]: '))).trim() || '1';
      if (!['1', '2', '3'].includes(updateChoice)) {
        console.log(c.red('  → Please enter 1, 2 or 3'));
      }
    }

    if (updateChoice === '3') {
      console.log('');
      console.log(c.dim('  Aborted. Nothing changed.'));
      console.log('');
      rl.close();
      return;
    }

    await installFiles(claudeBase, isGlobal, updateChoice === '1');
  } else {
    await installFiles(claudeBase, isGlobal, true);
  }

  rl.close();

  // ── Done ──────────────────────────────────────────────────────────────────
  console.log('');
  console.log(c.green('  ✓ ') + c.bold('red · proto installed successfully'));
  console.log('');

  if (isGlobal) {
    console.log(c.dim('  Open any project in Claude Code and run:'));
    console.log('');
    console.log(`  ${c.cyan('/red-proto:create')}   ${c.dim('← installs framework into your project')}`);
  } else {
    console.log(c.dim('  Open this project in Claude Code and run:'));
    console.log('');
    console.log(`  ${c.cyan('/red-proto:create')}   ${c.dim('← sets up project structure + design system')}`);
  }

  console.log('');
  console.log(c.dim('  Then start with:'));
  console.log('');
  console.log(`  ${c.cyan('/red-proto:sparring')}   ${c.dim('← describe your idea')}`);
  console.log('');
  console.log('  ' + c.dim('─'.repeat(48)));
  console.log('');
}

// ─── File copy logic ─────────────────────────────────────────────────────────

async function installFiles(claudeBase, isGlobal, noClobber) {
  const commandsDir = join(claudeBase, 'commands', 'red-proto');
  const agentsDir   = join(claudeBase, 'agents');
  const projectRoot = process.cwd();

  await mkdir(commandsDir, { recursive: true });
  await mkdir(agentsDir,   { recursive: true });

  const srcCommands = join(PACKAGE_ROOT, 'commands', 'red-proto');
  let copied = 0;
  let skipped = 0;

  // Copy entire red-proto commands folder
  const { readdir } = await import('fs/promises');
  const commandFiles = await readdir(srcCommands);
  for (const file of commandFiles) {
    const dest = join(commandsDir, file);
    const alreadyExists = await exists(dest);
    if (noClobber && alreadyExists) { skipped++; continue; }
    await cp(join(srcCommands, file), dest);
    copied++;
  }

  const srcAgents = join(PACKAGE_ROOT, 'agents');
  for (const file of AGENT_FILES) {
    const dest = join(agentsDir, file);
    const alreadyExists = await exists(dest);
    if (noClobber && alreadyExists) { skipped++; continue; }
    await cp(join(srcAgents, file), dest);
    copied++;
  }

  if (isGlobal) {
    // Global install: copy commands + agents + docs + design-system to
    // ~/.claude/templates/red-create-prototyp-project/ so that /red-proto:create
    // can later copy them into any project
    const templateBase  = join(homedir(), '.claude', 'templates', 'red-create-prototyp-project');
    const templateCmds  = join(templateBase, 'commands', 'red-proto');
    const templateAgents = join(templateBase, 'agents');
    await mkdir(templateCmds,   { recursive: true });
    await mkdir(templateAgents, { recursive: true });

    // Keep template commands + agents in sync with installed versions
    for (const file of commandFiles) {
      await cp(join(srcCommands, file), join(templateCmds, file), { force: true, errorOnExist: false });
    }
    for (const file of AGENT_FILES) {
      await cp(join(srcAgents, file), join(templateAgents, file), { force: true, errorOnExist: false });
    }

    // Copy docs (templates, SCAFFOLDING, CONVENTIONS) + design-system into templates/
    const srcDocs = join(PACKAGE_ROOT, 'docs');
    await cp(srcDocs, join(templateBase, 'docs'), { recursive: true, force: true, errorOnExist: false });

    const srcDS = join(PACKAGE_ROOT, 'design-system');
    await cp(srcDS, join(templateBase, 'design-system'), { recursive: true, force: true, errorOnExist: false });
  }

  // If local install: also set up project structure + design system + docs
  if (!isGlobal) {
    const dirs = ['research', 'features', 'flows', 'bugs', 'docs', 'projekt',
                  'design-system/tokens', 'design-system/components',
                  'design-system/patterns', 'design-system/screens'];
    for (const dir of dirs) {
      await mkdir(join(projectRoot, dir), { recursive: true });
    }
    const srcDS = join(PACKAGE_ROOT, 'design-system');
    await cp(srcDS, join(projectRoot, 'design-system'), { recursive: true, force: !noClobber, errorOnExist: false });

    // Copy framework docs to .claude/red-proto/ (templates, SCAFFOLDING, CONVENTIONS)
    const srcDocs = join(PACKAGE_ROOT, 'docs');
    await mkdir(join(projectRoot, '.claude', 'red-proto'), { recursive: true });
    await cp(srcDocs, join(projectRoot, '.claude', 'red-proto'), { recursive: true, force: !noClobber, errorOnExist: false });
  }

  console.log('');
  if (copied > 0)  console.log(c.green(`  ✓ ${copied} file(s) installed`));
  if (skipped > 0) console.log(c.dim(`  → ${skipped} file(s) skipped (already exist)`));
}

main().catch(err => {
  console.error(c.red('\n  Error: ') + err.message);
  process.exit(1);
});
