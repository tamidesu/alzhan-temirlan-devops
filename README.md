# alzhan-temirlan-devops

Individual laboratory project for the DevOps course.

- Name: Temirlan
- Surname: Alzhan
- Group: IT2-2307
- Student ID: 38372

## Environment

Ubuntu 26.04 LTS under WSL2 on Windows, Python 3, Git, Docker Desktop
with Ubuntu WSL integration and the Docker Compose plugin.
Jenkins runs as a Linux service with Git, Python 3, curl and Docker access.
Do not install a second Docker Engine alongside the Desktop integration.

## Project structure

- `app/main.py`: personalized HTTP application; `/` shows student information and `/health` returns `OK`.
- `app/test_main.py`: three automated tests for defaults, environment overrides and rendered output.
- `app/version.txt`: application version.
- `scripts/Alzhan_Temirlan_system.sh`: student and system information, including a student-file existence check.
- `Alzhan_Temirlan_info.txt`: student information for the Linux demonstration.
- `config/student.json`: application defaults.
- `config/app.conf`: reference settings for the directory-structure exercise; the application does not read this file.
- `private.txt`, `public.txt`: dummy text for the Linux permissions exercise.
- `Dockerfile`, `.dockerignore`: container image build configuration.
- `docker-compose.yml`: local application deployment.
- `Jenkinsfile`: compilation, tests, image build and deployment pipeline.
- `.env.example`: public sample runtime values.
- `logs/`, `backup/`, `.env`, `practice_task1/`: local files excluded from Git.

Git does not preserve empty directories or full Unix permission modes.

## Set up a local checkout

```bash
git clone https://github.com/tamidesu/alzhan-temirlan-devops.git
cd alzhan-temirlan-devops
mkdir -p logs backup
cp .env.example .env
chmod +x scripts/Alzhan_Temirlan_system.sh
chmod 600 private.txt
chmod 644 public.txt
```

The original Linux exercise uses `/home/temirlan/devops/alzhan_temirlan`.
The application and system script also work from another checkout path.
The files used for the log and disposable-file exercises are created locally;
their generated contents are not required to run the application.
Use dummy data for permission demonstrations: local mode 600 does not make a
file published on GitHub private.

## Run and test without Docker

```bash
bash -n scripts/Alzhan_Temirlan_system.sh
./scripts/Alzhan_Temirlan_system.sh
python3 -m compileall -q app
python3 -m unittest discover -s app -p 'test_*.py' -v
python3 app/main.py
```

Keep the last command running, then use another terminal:

```bash
curl -fsS --max-time 5 http://127.0.0.1:8000/
curl -fsS --max-time 5 http://127.0.0.1:8000/health
```

Stop the foreground server with Ctrl+C before deploying a container on port 8000.
The Python application reads `config/student.json` and overrides its defaults
with `STUDENT_NAME`, `STUDENT_SURNAME`, `STUDENT_GROUP` and `STUDENT_ID`.
It does not automatically load `.env`; Compose loads that file explicitly.
`PORT` changes the application listening port; the provided Docker configuration
uses port 8000. `app/version.txt` supplies the displayed version.

## Docker

```bash
docker build --progress=plain -t alzhan-temirlan-devops:latest .
docker run -d --name alzhan-temirlan-container \
  -p 127.0.0.1:8000:8000 \
  --env-file .env \
  alzhan-temirlan-devops:latest
docker ps
docker logs alzhan-temirlan-container
curl -fsS --max-time 5 http://127.0.0.1:8000/
docker exec alzhan-temirlan-container python --version
```

Allow a moment for application startup before checking HTTP. Changing runtime
environment variables requires recreating the container, without rebuilding
the image. Stop and remove this container before switching deployment methods:

```bash
docker stop alzhan-temirlan-container
docker rm alzhan-temirlan-container
```

The simple application may require Docker's forced termination after the stop
timeout; exit code 137 alone does not establish an out-of-memory event.

## Docker Compose

With `.env` copied from `.env.example` and port 8000 available:

```bash
docker compose config
docker compose up -d --build
docker compose ps
docker compose logs app
curl -fsS --max-time 5 http://127.0.0.1:8000/
docker compose down
```

Compose, manual Docker commands and Jenkins share the same fixed container name
and host port. Run one deployment method at a time; use `docker compose down`
before deploying through Jenkins.

## Jenkins

Create the Pipeline job `Alzhan_Temirlan_DevOps` with:

- Definition: **Pipeline script from SCM**
- SCM: **Git**
- Repository URL: `https://github.com/tamidesu/alzhan-temirlan-devops.git`
- Branch: `*/main`
- Script Path: `Jenkinsfile`

The Jenkins agent needs Python 3, Git, Docker and curl 7.71.0 or newer.
Its service account must be able to access the Docker daemon, and Docker Desktop
must be running. Public repository checkout does not require GitHub credentials.
Select **Build Now** after pushing a change. A webhook is optional.

Stages:

1. **Checkout** retrieves the source and records its full Git commit.
2. **Build** checks Python compilation.
3. **Test** runs all three unit tests.
4. **Docker Build** creates an image tagged with the first 12 commit characters
   and `latest`, and adds the full commit as `org.opencontainers.image.revision`.
5. **Docker Run** replaces the demonstration container, passes the four student
   variables, retries the initial HTTP request, checks the returned identity,
   checks `/health` and prints logs and image IDs.

The pipeline disables concurrent builds of this job and has a 15-minute timeout.
A failed command fails the build and skips later normal stages. Diagnostic
failure logs do not turn a failure into success. The deployed container remains
running after a successful build.

## Trace a source change to deployment

Edit `app/version.txt`, inspect the diff, commit the change and push `main`.
Run Jenkins again and verify the new version through HTTP. The `development`
branch preserves the earlier version-change and merge demonstration.

For the final successful build, compare the Jenkins checkout revision with:

```bash
git rev-parse HEAD
git ls-remote origin refs/heads/main
docker image inspect alzhan-temirlan-devops:latest \
  --format '{{ index .Config.Labels "org.opencontainers.image.revision" }}'
docker image inspect alzhan-temirlan-devops:latest --format '{{.Id}}'
docker inspect alzhan-temirlan-container --format '{{.Image}}'
```

The three Git revision values must agree. The two image IDs must agree with each
other; an image ID is a different identifier from a Git commit hash.

## Local files and security

`.gitignore` excludes logs, backups, `.env`, Python caches and disposable exercise
files. `.dockerignore` excludes local-only files from the image build context.
Keep real secrets out of the repository, screenshots and video.
This is a local teaching application, without production authentication or TLS.
