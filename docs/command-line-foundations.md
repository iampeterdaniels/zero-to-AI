# Command Line Foundations for Zero-to-AI

**Audience:** Zero-to-AI learners, including those with little or no command-line experience  
**Goal:** Build confidence using the command line by learning how to orient yourself, choose the right shell for your operating system, and safely follow Zero-to-AI instructions.

> 📄 **Quick reference:** Keep the [Command Line Cheat Sheet](command-line-cheat-sheet.md) open during this and future Zero-to-AI sessions.

---

## Why This Session Exists

Zero-to-AI uses real developer tools like Git and Python. Many of those tools are driven through the command line. This session is not about becoming a command-line expert—it’s about learning just enough to:

- Know which terminal to use on your computer
- Know where you are on your machine
- Know how to find and move into the right folder
- Recover when you feel “lost”

If you can do those things, you can successfully complete the rest of the course.

---

## What Is a Shell?

A **shell** is a text-based way to give instructions to your computer.

Different shells exist for different operating systems and purposes. In Zero-to-AI, we intentionally focus on a small set of shells so everyone is learning from the same baseline and instructions are predictable.

---

## The Shells We Use in Zero-to-AI

### Git Bash (Windows)

**Best for:**
- Git commands (clone, pull, etc.)
- Unix-style navigation

**How to recognize it:**
- Prompt usually includes `MINGW64`

**Script types:**
- Runs `.sh` scripts

---

### PowerShell (Windows)

**Best for:**
- Windows-native scripting
- Zero-to-AI setup scripts

**How to recognize it:**
- Prompt starts with `PS C:\...>`

**Script types:**
- Runs `.ps1` scripts

---

### Terminal (macOS)

**Best for:**
- All Zero-to-AI command line tasks on Mac
- Git and Unix-style navigation

**How to recognize it:**
- App name: **Terminal**
- Default shell: `zsh`

**Commands:**
- Uses the same commands as Git Bash:
  - `pwd`
  - `ls`
  - `cd`
  - `git`

> If you’re on a Mac, **Terminal is your Git Bash equivalent**.  
> You do not need PowerShell for Zero-to-AI.

---

### Important Note

Running the *right command in the wrong shell* is one of the most common beginner mistakes—and it’s completely normal. When something doesn’t work, the first thing to check is which shell you’re using.

---

## Command Line Survival Skills

These commands are safe to use and work across Zero-to-AI sessions. You don’t need to memorize them—this page is your reference.

### Where am I?

```shell
pwd
```

### What’s in this folder?

**Git Bash / macOS Terminal**
```shell
ls
```

**PowerShell**
```powershell
dir
```

### How do I move into a folder?

```shell
cd folder-name
```

Go up one level:
```shell
cd ..
```

---

### The Recovery Loop

If you ever feel lost, do this:

```text
pwd
ls / dir
cd ..
pwd
```

Don’t guess. Inspect first, then move.

---

## Checking That Git Is Available

```shell
git --version
```

If you see a version number, Git is installed and ready.

---

## File Types You’ll See in Zero-to-AI

| File Type | Run It In |
|----------|-----------|
| `.ps1` | PowerShell (Windows only) |
| `.sh` | Git Bash (Windows) or Terminal (macOS) |

---

## Keeping Your Zero-to-AI Repo Up to Date

The Zero-to-AI course content may change between sessions. Your local copy does **not** update automatically.

Only do this **if instructed**:

```shell
git pull
```

If it fails, stop and ask for help.

---

## Tools You Might Hear About (But Don’t Need Right Now)

- **PowerShell ISE** – An advanced PowerShell editor some people use later
- **GitHub Desktop** – A UI-based Git tool

For Zero-to-AI, we intentionally stick to **Git Bash, PowerShell, and macOS Terminal** so everyone shares the same learning experience.

---

## Final Reassurance

You are not expected to be “good at the command line.”

If you can:
- Open the correct shell for your operating system
- Run `pwd`
- Run `ls` or `dir`
- Use `cd` to move into a folder

You are fully prepared for the rest of Zero-to-AI.
