const API_URL = "http://localhost:3000";

function showRegister() {
    document.getElementById("auth-container").style.display = "none";
    document.getElementById("register-container").style.display = "block";
}

function showLogin() {
    document.getElementById("register-container").style.display = "none";
    document.getElementById("auth-container").style.display = "block";
}

async function register() {
    const username = document.getElementById("reg-username").value;
    const password = document.getElementById("reg-password").value;
    
    const res = await fetch(`${API_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });
    
    const data = await res.json();
    alert(data.message);
    if (res.ok) showLogin();
}

async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    
    const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });
    
    const data = await res.json();
    if (res.ok) {
        localStorage.setItem("role", data.role);
        document.getElementById("role-display").innerText = `Role: ${data.role}`;
        document.getElementById("username-login").innerText = `Username: ${username}`;
        document.getElementById("auth-container").style.display = "none";
        document.getElementById("dashboard").style.display = "block";
    } else {
        alert(data.error);
    }
}

async function fetchStudents() {
    try {
        const res = await fetch(`${API_URL}/students`, {
            method: "GET",
            headers: { "Content-Type": "application/json" },
            credentials: "include"  // <---- Add this
        });
        

        if (!res.ok) throw new Error(await res.text()); 

        const data = await res.json();
        document.getElementById("students-list").innerHTML = data.map(student => `
            <p>${student.roll} - ${student.name}, ${student.branch}</p>
        `).join("");
    } catch (error) {
        console.error("Error fetching students:", error);
        alert(error.message);
    }
}

document.getElementById("student-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default submission

    // Fetch input values
    const name = document.getElementById("student-name").value.trim();
    const age = document.getElementById("student-age").value.trim();
    const roll = document.getElementById("student-roll").value.trim();
    const branch = document.getElementById("student-branch").value.trim();
    const hometown = document.getElementById("student-hometown").value.trim();

    // Check if any field is empty
    if (!name || !age || !roll || !branch || !hometown) {
        alert("Please fill in all fields before submitting.");
        return;
    }

    // Call the addStudent function if validation passes
    addStudent({ roll, name, age, branch, hometown });
});

document.getElementById("Role-Assigner").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default submission

    // Fetch input values
    const username = document.getElementById("assign-role-username").value.trim();
    const role = document.getElementById("assign-role-role").value.trim();

    // Call the addStudent function if validation passes
    assignRole({ username, role});
});

async function addStudent(student) {
    //authentication:
    let role = document.getElementById("role-display").innerText;

    //check if this guy has right to edit:
    role = role.slice(6);

    if (role=="viewer") {
        alert("Viewer doesn't have edit permissions");
    }
    else {
        try {
            const res = await fetch(`${API_URL}/students`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(student),
                credentials: "include"
            });

            if (!res.ok) throw new Error(await res.text());

            alert("Student added successfully!");
            document.getElementById("student-form").reset(); // Clear form after success
            fetchStudents(); // Refresh student list
        } catch (error) {
            console.error("Error adding student:", error);
            alert(error.message);
        }
    }
}

async function assignRole(body) {
    //authentication:
    let role = document.getElementById("role-display").innerText;

    //check if this guy has right to edit:
    role = role.slice(6);

    console.log(body.role);
    if (role=="viewer" || role=="editor") {
        alert("Viewer or Editor doesn't have role-assignment permissions");
    }
    else if(body.role!="viewer" && body.role!="editor" && body.role!="admin") {
        alert("Not a valid role provided");
    }
    else {
        try {
            const res = await fetch(`${API_URL}/assign-role`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body),
                credentials: "include"
            });

            if (!res.ok) throw new Error(await res.text());

            alert("Role edited successfully!");
        } catch (error) {
            console.error("Error adding student:", error);
            alert(error.message);
        }
    }
}

async function logout() {
    try {
        const response = await fetch(`${API_URL}/logout`, {
            method: "GET",
            credentials: "include",
        });

        const data = await response.json(); // Check server response

        localStorage.clear();

        document.getElementById("dashboard").style.display = "none";
        document.getElementById("auth-container").style.display = "block";
    } catch (error) {
        console.error("Logout failed:", error);
    }
}


