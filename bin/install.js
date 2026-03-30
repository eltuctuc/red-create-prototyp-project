#!/usr/bin/env node

import { createInterface } from 'readline';
import { cp, mkdir, access } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { homedir } from 'os';
import { createReadStream } from 'fs';

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

// ─── Main ────────────────────────────────────────────────────────────────────

async function main() {
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

  console.log('');

  // ── Step 2: Confirm if already installed ──────────────────────────────────
  const commandsDir = join(claudeBase, 'commands');
  const alreadyInstalled = await exists(join(commandsDir, 'red:proto.md'));

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
    console.log(`  ${c.cyan('/red:proto')}   ${c.dim('← installs framework into your project')}`);
  } else {
    console.log(c.dim('  Open this project in Claude Code and run:'));
    console.log('');
    console.log(`  ${c.cyan('/red:proto')}   ${c.dim('← sets up project structure + design system')}`);
  }

  console.log('');
  console.log(c.dim('  Then start with:'));
  console.log('');
  console.log(`  ${c.cyan('/red:proto-sparring')}   ${c.dim('← describe your idea')}`);
  console.log('');
  console.log('  ' + c.dim('─'.repeat(48)));
  console.log('');
}

// ─── File copy logic ─────────────────────────────────────────────────────────

async function installFiles(claudeBase, isGlobal, noClobber) {
  const commandsDir = join(claudeBase, 'commands');
  const agentsDir = join(claudeBase, 'agents');
  const projectRoot = process.cwd();

  // Create dirs
  await mkdir(commandsDir, { recursive: true });
  await mkdir(agentsDir, { recursive: true });

  const copyOpts = { recursive: true, force: !noClobber, errorOnExist: false };

  // Commands
  const srcCommands = join(PACKAGE_ROOT, 'commands');
  const files = [
    'red:proto.md',
    'red:proto-workflow.md',
    'red:proto-sparring.md',
    'red:proto-dev-setup.md',
    'red:proto-research.md',
    'red:proto-requirements.md',
    'red:proto-flows.md',
    'red:proto-ux.md',
    'red:proto-architect.md',
    'red:proto-dev.md',
    'red:proto-qa.md',
  ];

  let copied = 0;
  let skipped = 0;

  for (const file of files) {
    const dest = join(commandsDir, file);
    const alreadyExists = await exists(dest);
    if (noClobber && alreadyExists) {
      skipped++;
      continue;
    }
    await cp(join(srcCommands, file), dest);
    copied++;
  }

  // Agents
  const srcAgents = join(PACKAGE_ROOT, 'agents');
  const agents = ['frontend-developer.md', 'backend-developer.md', 'qa-engineer.md', 'ux-reviewer.md'];

  for (const file of agents) {
    const dest = join(agentsDir, file);
    const alreadyExists = await exists(dest);
    if (noClobber && alreadyExists) {
      skipped++;
      continue;
    }
    await cp(join(srcAgents, file), dest);
    copied++;
  }

  // If local install: also set up project structure + design system
  if (!isGlobal) {
    const dirs = ['research', 'features', 'flows', 'bugs', 'docs', 'projekt',
                  'design-system/tokens', 'design-system/components',
                  'design-system/patterns', 'design-system/screens'];
    for (const dir of dirs) {
      await mkdir(join(projectRoot, dir), { recursive: true });
    }
    const srcDS = join(PACKAGE_ROOT, 'design-system');
    await cp(srcDS, join(projectRoot, 'design-system'), { recursive: true, force: !noClobber, errorOnExist: false });
  }

  console.log('');
  if (copied > 0)  console.log(c.green(`  ✓ ${copied} file(s) installed`));
  if (skipped > 0) console.log(c.dim(`  → ${skipped} file(s) skipped (already exist)`));
}

main().catch(err => {
  console.error(c.red('\n  Error: ') + err.message);
  process.exit(1);
});
