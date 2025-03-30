const bcrypt = require('bcrypt');

bcrypt.hash("user@123", 10, (err, hash) => {
    if (err) console.error(err);
    console.log("Hashed password:", hash);
});
