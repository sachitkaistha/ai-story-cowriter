import subprocess
import streamlit as st
import pandas as pd

st.set_page_config(page_title= "Remote Docker Manager", page_icon="🦈")
st.title("🐳 Remote Docker via SSH")

st.sidebar.header("🔐 SSH connection")
ssh_ip = st.sidebar.text_input("Remote Host ip", placeholder="eg. 192.168.1.10")
ssh_username = st.sidebar.text_input("Username", placeholder = "root")

def run_ssh_cmd(cmd, show_output=True):
    full_cmd = f"ssh {ssh_username}@{ssh_ip} {cmd}"
    st.code(f"$ {full_cmd}")

    try:
        result = subprocess.check_output(full_cmd, shell=True, text=True)
        if show_output:
            st.code(result)
        return result
    except subprocess.CalledProcessError as e:
        error_output = e.output or str(e)
        if show_output:
            st.error(f"❌ Error:\n{error_output}")
        return error_output

if ssh_ip and ssh_username:
    st.success("SSH connection ready")

    menu = ["List Images", "List Containers", "Pull Image", "Run Image", "Stop Container",
            "Start container", "Remove container", "Push to DockerHub", "Install Docker"]
    
    choice = st.selectbox("Select Docker Actions", menu)

    if choice == "Pull Image":
        image = st.text_input("Enter Image Name to Pull")
        if st.button("Pull"):
            run_ssh_cmd(f"docker pull {image}")

    elif choice == "List Images":
        if st.button("Images"):
            run_ssh_cmd("docker images")

    elif choice == "List Containers":
        if st.button("Containers"):
            run_ssh_cmd("docker ps -a")

    elif choice == "Run Image":
        image = st.text_input("Enter Image Name to Run")
        name = st.text_input("Enter Container Name")
        if st.button("Run"):
            run_ssh_cmd(f"docker run -itd --name {name} {image}")

    elif choice == "Stop Container":
        image = st.text_input("Enter Container Name to Stop")
        if st.button("Stop"):
            run_ssh_cmd(f"docker stop {image}")

    elif choice == "Start Container":
        image = st.text_input("Enter Container Name to Start")
        if st.button("Start"):
            run_ssh_cmd(f"docker start {image}")

    elif choice == "Remove container":
        image = st.text_input("Enter Container Name to Remove")
        if st.button("Remove"):
            run_ssh_cmd(f"docker rm -f {image}")

    elif choice == "Push to DockerHub":
        username = st.text_input("Enter DockerHub Username")
        image = st.text_input("Enter Image Name")
        name = st.text_input("Enter pushed Image Name")
        if st.button("Push"):
            run_ssh_cmd(f"docker tag {image} {username}/{name}")
            run_ssh_cmd(f"docker push {username}/{name}")

    elif choice == "Install Docker":
        if st.button("Install Docker"):
            run_ssh_cmd("sudo dnf -y install dnf-plugins-core")
            run_ssh_cmd("sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo")
            run_ssh_cmd("sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin")
            run_ssh_cmd("sudo systemctl start docker && sudo systemctl enable docker")
    else:
        st.warning("Please Enter SSH IP and Username in the Side Bar")
