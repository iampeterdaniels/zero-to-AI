# Zero-to-AI Command Line Cheat Sheet

> Keep this open during Zero-to-AI sessions. You are **not** expected to memorize these commands.

> This cheat sheet supports the **Command Line Foundations** session.

---

## Which terminal should I use?

- **Windows**
  - Git Bash → Git commands, Unix-style navigation
  - PowerShell → Windows setup scripts (`.ps1`)
- **macOS**
  - Terminal → Use this for all Zero-to-AI tasks

> macOS Terminal behaves like **Git Bash**. You do not need PowerShell on Mac.

---

## The three questions that fix most problems

### Where am I?
```shell
pwd
```

### What’s here?

**Git Bash / macOS Terminal**
```shell
ls
```

**PowerShell**
```powershell
dir
```

### How do I move?
```shell
cd folder-name
```

Go up one level:
```shell
cd ..
```

---

## The recovery loop

If you feel lost, do this:

```text
pwd
ls / dir
cd ..
pwd
```

Inspect first. Don’t guess.

---

## Checking Git

```shell
git --version
```

If you see a version number, Git is installed.

---

## File types you’ll see

| File | Run it in |
|------|-----------|
| `.ps1` | PowerShell (Windows only) |
| `.sh` | Git Bash (Windows) or Terminal (macOS) |

---

## Keeping your repo up to date

Only do this **if instructed**:

```shell
git pull
```

If it fails, stop and ask for help.

---

> If you can run `pwd`, `ls`/`dir`, and `cd`, you’re ready for Zero-to-AI.
