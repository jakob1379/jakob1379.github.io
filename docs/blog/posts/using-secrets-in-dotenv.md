---
authors:
 - jsg
date: 2025-11-13
---

As a first try on writing and article I thought of many topics that could be fun, but starting with
something simple, that I actually find myself using more often, might be the better topic to start
off with. So here goes nothing!

---

# Managing Secrets in Dotenv Files with the Kerying #

When developing software, we often fine ourselves relying on `.env` files to store configuration and
secrets. But this common practice has some serious drawbacks as anyone with access to your computer
can read these plaintext passwords.

The problem gets worse when:
- You accidentally commit a `.env` file to version control
- You need to share configuration across team members
- You must rotate compromised keys across multiple projects

A better approach exists: using your system's keyring. Most operating systems include encrypted
vaults like [GnomeKeyring](https://wiki.gnome.org/Projects/GnomeKeyring) or [KWalletManager](https://apps.kde.org/en-gb/kwalletmanager5/) that store WiFi passwords and browser logins
behind a master password. Many tools for interacting with the keyring exists, but I prefer the
simplicity of the cli-tool [keyring](https://github.com/jaraco/keyring) for programmatic interactions.

Install however you like, but for the sake of inclusion, here is one way:

```bash
# Install the keyring tool
uv tool install keyring
```

We can then proceed to look at common `.env` that looks something like this:

```bash
foo=1
bar=2
DB_PASSWORD=pass123
```

Now, with the keyring available to our fingertips, we can store in the keyring like so:

```bash
keyring --help
usage: keyring ... [{get,set,...}] [service] [username]
```

I have truncated things that are not important, for now, as we are only concerned about settings and
getting our secrets. I usually prefer the naming convention for *service* as the service or project
I am working on or using e.g. *my-service* or *name-of-online-service*, and then *username* as a
descriptive name for what the secret is used for, e.g. *db-admin-pass* or *api_key*. First we add
the secret to the keyring:


```bash
❯ keyring set my-service db-admin-password
Password for 'db-admin-password' in 'my-service': *******
```

Then proceed to reference it in your `.env` file:

```bash
foo=1
bar=2
DB_PASSWORD=$(keyring get my-service db-admin-password)
```

This approach gives you a few things:
- Centralized secret management
- Easy key rotation (update once, apply everywhere)
- Shareable configuration without exposing secrets
- Better security than plaintext files

The keyring acts as a set-and-forget solution that keeps your secrets secure while maintaining the
convenience of `.env` files. Though you still need to source the file to actually get the secret
available in the environment.

The automation of this will be in the next post, I think.
