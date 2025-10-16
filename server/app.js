require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bodyParser = require('body-parser');

const authRoutes = require('./routes/auth');
const userRoutes = require('./routes/users');
const protectedRoutes = require('./routes/protected');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(bodyParser.json());

// Свързване с MongoDB
mongoose.connect(process.env.MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
.then(() => console.log("Свързано с MongoDB"))
.catch(err => console.error("Грешка при свързване:", err));

app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);
app.use('/api/protected', protectedRoutes);

app.listen(PORT, () => {
    console.log(`Сървърът работи на порт ${PORT}`);
});
