1<div align="center">

# jakob1379.github.io The Page

  [![Deploy to gh-pages](https://github.com/jakob1379/jakob1379.github.io/actions/workflows/gh-deploy.yml/badge.svg)](https://github.com/jakob1379/jakob1379.github.io/actions/workflows/gh-deploy.yml)
  [![Website](https://img.shields.io/badge/Website-jakob1379.github.io-blue.svg)](https://jakob1379.github.io/)

</div>

This repository hosts the source code for my personal website and blog. It's built using [Zensical](https://zensical.org/) and automatically deployed to GitHub Pages using Github Actions.

## Development Setup

### Prerequisites

- [Nix](https://nixos.org/download/) (for reproducible development environment)
- [Git](https://git-scm.com/)

### Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/jakob1379/jakob1379.github.io.git
   cd jakob1379.github.io
   ```

2. Enter the Nix development shell:

   ```bash
   nix develop
   ```

   This will provide all necessary tools (uv, pre-commit, etc.).

3. Install Python dependencies:

   ```bash
   uv sync
   ```

4. Install pre-commit hooks:

   ```bash
   poe setup
   ```

### Local Development

- **Serve the site locally**:

  ```bash
  poe serve
  ```

  The site will be available at <http://localhost:8888>

- **Build the site**:

  ```bash
  poe build
  ```

  This generates the static site in the `site/` directory.

- **Build with minification** (production):

  ```bash
  poe build_prod
  ```

## Adding Blog Posts

1. Create a new Markdown file in `docs/blog/posts/` with the following frontmatter:

   ```yaml
   ---
   authors:
    - jsg
   date: YYYY-MM-DD
   ---
   ```

2. Write your content using Markdown with Zensical extensions (admonitions, tabs, etc.).

3. The post will automatically appear in the blog index.

## Quality Assurance

### Pre-commit Hooks

This repository uses pre-commit hooks to ensure code quality. Hooks run automatically on `git commit` and check for:

- Secret leakage (gitleaks)
- Markdown linting
- YAML/TOML syntax
- Spell checking

To run hooks manually:

```bash
pre-commit run --all-files
```

### CI/CD Pipeline

The GitHub Actions workflow (`gh-deploy.yml`):

1. Builds the CV (RenderCV)
2. Builds the Zensical site
3. Minifies assets (HTML, CSS, JS)
4. Deploys to GitHub Pages
5. Creates PR previews with smokeshow (`preview.yml`)

Build artifacts are cached between runs for faster deployments.

## Pull Request Previews

When a pull request is opened, a temporary preview of the static site is automatically built and deployed using [smokeshow](https://github.com/samuelcolvin/smokeshow). This allows you to visually review changes before merging.

### Setting up previews

1. Generate an upload key for smokeshow:

   ```bash
   nix develop -c smokeshow generate-key
   ```

2. Add the generated key as a repository secret named `SMOKESHOW_AUTH_KEY` in your GitHub repository settings (Settings → Secrets and variables → Actions → New repository secret).

Once the secret is set, future pull requests will have a "Preview site" status with a link to the ephemeral preview site. The preview will expire after 30 days.

## Deployment

Deployment happens automatically when changes are pushed to the `main` branch. To deploy manually:

```bash
poe deploy
```

This will build the site (with minification) and push to the `gh-pages` branch.

## Project Structure

```bash
├── docs/                   # Source content (Markdown files, assets)
│   ├── blog/               # Blog posts
│   ├── stylesheets/        # Custom CSS
│   └── javascripts/        # Custom JavaScript
├── cv/                     # CV source (YAML) and RenderCV configuration
├── overrides/              # Zensical theme overrides
├── scripts/                # Build utilities (minification)
├── pyproject.toml          # Python dependencies and Poe tasks
├── zensical.toml           # Zensical configuration
└── flake.nix               # Nix development environment
```

## Contributing

Found a typo or have a suggestion? Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
