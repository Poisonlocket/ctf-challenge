from fastapi import FastAPI, Request, Response, HTTPException
import subprocess

app = FastAPI()

FLAG = "quack{0ne_c00k1e_pl31se}"

# create flag file when container/app starts
@app.on_event("startup")
def create_flag():
    with open("./flag.txt", "w") as f:
        f.write(FLAG)


@app.get("/")
def root():
    return {
        "message": "Welcome to the Cookie dispenser Service for Ducks. Sadly we dont have enough funding yet to afford a Frontend Dev. Our Backend engineer also was kind of underpaid so we hope he did his job right and didnt leave any vulnerabilitys. Anyways, head to /cookie for a free cookie, if you dont get one, an admin needs to refill them at /admin"
    }


@app.get("/cookie")
def get_cookie(response: Response, username: str = "guest"):
    response.set_cookie(
        key="session",
        value=username,
        httponly=False
    )

    return {
        "message": "Here is your cookie 🍪",
        "username": username
    }


@app.get("/admin")
def admin(request: Request):
    info = ""
    output = ""
    session = request.cookies.get("session")

    if not session:
        raise HTTPException(status_code=401, detail="No cookie found")

    username = session

    try:
        if username == "guest":
            info = "didnt get paid enough to handle this securely this code really makes me evaluate my choices"
            output = ""
            print("no")
        else:
            print("yes")
            info = "didnt get paid enough to handle this securely this code really makes me evaluate my choices"
            args = username.split()
            command_exec = subprocess.run(args, capture_output=True, text=True)
            output = command_exec.stdout + command_exec.stderr
    except Exception:
        info = "didnt get paid enough to handle this securely this code really makes me evaluate my choices"
        output = ""

    return {
        "username": username,
        "message": "Welcome to the admin panel",
        "admin_info": info + " " + output
    }