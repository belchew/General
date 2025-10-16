const jwt = require('jsonwebtoken');
const User = require('../models/User');

const authenticateToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];
    if (!token) return res.status(401).json({ message: "Не сте логнат" });

    jwt.verify(token, process.env.JWT_SECRET, (err, userData) => {
        if (err) return res.status(403).json({ message: "Невалиден токен" });
        req.user = userData;
        next();
    });
};

const requireAdmin = async (req, res, next) => {
    // user в req.user съдържа id и role
    const user = await User.findById(req.user.id);
    if (!user) {
        return res.status(404).json({ message: "Потребителят не е намерен" });
    }
    if (user.role !== 'admin') {
        return res.status(403).json({ message: "Липса на права за достъп" });
    }
    next();
};

module.exports = { authenticateToken, requireAdmin };
