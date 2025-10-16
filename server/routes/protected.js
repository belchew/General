const express = require('express');
const router = express.Router();
const { authenticateToken } = require('../middleware/authMiddleware');

// Този маршрут може да върне информация, която фронтенд ще използва да зареди stream
router.get('/stream-info', authenticateToken, (req, res) => {
    // Може да върнеш URL на stream или конфигурация
    res.json({
        streamUrl: process.env.STREAM_URL || "https://example.com/live/stream.m3u8"
    });
});

module.exports = router;
