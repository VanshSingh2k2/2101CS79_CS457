const express = require("express");
const fs = require("fs");
const bcrypt = require("bcryptjs");
const session = require("express-session");

const app = express();
const PORT = 3000;

const cors = require("cors");

app.use(cors({
    origin: "http://localhost:50000", // Replace with your frontend origin
    credentials: true // Allow cookies and credentials
}));


app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(session({
    secret: "secret_key",
    resave: false,
    saveUninitialized: true
}));

const USERS_FILE = __dirname + "/users.json";;
const DB_FILE = __dirname + "/stud_info.json";

// Load users from JSON
const loadUsers = () => {
    try {
        if (!fs.existsSync(USERS_FILE)) {
            console.log("users.json not found. Creating a new one.");
            fs.writeFileSync(USERS_FILE, JSON.stringify({}, null, 2), "utf-8"); // Create an empty object in the file
            return {};
        }
        const data = fs.readFileSync(USERS_FILE, "utf-8").trim(); // Trim to avoid accidental empty strings
        return data ? JSON.parse(data) : {}; // If empty, return an empty object
    } catch (err) {
        console.error("Error reading users.json:", err);
        return {}; // Return empty object instead of crashing
    }
};


const saveUsers = (users) => {
    try {
        console.log("Saving users to file:", users);
        fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2), "utf-8");
        console.log("✅ users.json updated successfully!");
    } catch (err) {
        console.error("❌ Error writing users.json:", err);
    }
};




// Load database
const loadDB = () => fs.existsSync(DB_FILE) ? JSON.parse(fs.readFileSync(DB_FILE, "utf-8")) : [];
const saveDB = (data) => {
    var existingData = fs.existsSync(DB_FILE) ? JSON.parse(fs.readFileSync(DB_FILE, "utf-8")) : [];
    existingData=data;
    fs.writeFileSync(DB_FILE, JSON.stringify(existingData, null, 2), "utf-8");
};


// Middleware to check authentication
const isAuthenticated = (req, res, next) => {
    console.log("Session Data:", req.session);
    if (req.session.user) next();
    else res.status(401).json({ error: "Unauthorized. Please login." });
};


// Middleware to check role
const hasRole = (role) => (req, res, next) => {
    if (req.session.user && req.session.user.role === role) next();
    else res.status(403).json({ error: "Forbidden. You don't have permission." });
};

// Register route
app.post("/register", async (req, res) => {
    const { username, password } = req.body;
    
    const users = loadUsers(); 
    console.log("Current users before registration:", users); // Debugging log
    
    if (users[username]) return res.status(400).json({ error: "User already exists." });

    const hashedPassword = await bcrypt.hash(password, 10);
    users[username] = { password: hashedPassword, role: "viewer" }; 
    console.log("Updated users:", users); // Debugging log

    saveUsers(users); // Saving users after update
    res.json({ message: "Registration successful." });
});


// Login route
app.post("/login", async (req, res) => {
    const { username, password } = req.body;
    const users = loadUsers();
    
    if (!users[username]) return res.status(400).json({ error: "User not found." });
    if (!await bcrypt.compare(password, users[username].password)) return res.status(401).json({ error: "Invalid credentials." });
    
    req.session.user = { username, role: users[username].role };
    res.json({ message: "Login successful", role: users[username].role, username: username});
});

// Logout route
app.get("/logout", (req, res) => {
    console.log("Logging out...");
    
    req.session.destroy((err) => {
        if (err) {
            console.error("Error destroying session:", err);
            return res.status(500).json({ error: "Logout failed" });
        }
        
        console.log("Session destroyed successfully.");
        res.json({ message: "Logged out." });
    });
});


// Admin assigns roles
app.post("/assign-role", (req, res) => {
    const { username, role } = req.body;
    const users = loadUsers();
    
    if (!users[username]) return res.status(404).json({ error: "User not found." });
    users[username].role = role;
    saveUsers(users);
    res.json({ message: `Role updated to ${role}` });
});

// ✅ FIXED: Fetch all students (GET /students)
app.get("/students", (req, res) => {
    const students = loadDB();
    res.json(students);
});

// ✅ FIXED: Add a student (POST /students, only Admin)
app.post("/students", (req, res) => {
    const students = loadDB();
    console.log(req.body);
    console.log(students);
    students.push(req.body)
    saveDB(students);
    res.json({ message: "Student added successfully." });
});

// Start server
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
