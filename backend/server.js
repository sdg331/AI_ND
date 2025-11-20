const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const User = require('./models/User'); // 모델 파일 경로 확인

const app = express();
const PORT = 5000;
const MONGO_URI = 'mongodb://localhost:27017/recipe-profile-db'; // MongoDB 주소

// 미들웨어
app.use(cors()); // 프론트엔드 요청 허용
app.use(express.json());

// DB 연결
mongoose.connect(MONGO_URI)
    .then(() => console.log('✅ MongoDB 연결 성공'))
    .catch(err => console.error('❌ MongoDB 연결 실패:', err));

// [초기 데이터 생성]
const seedUser = async () => {
    const count = await User.countDocuments();
    if (count === 0) {
        await User.create({
            email: "student@university.ac.kr",
            cook_goals: "건강한 식습관 만들기",
            skill_level: "초보",
            preferences: {
                favorite_ingredients: ["계란", "스팸"],
                disliked_ingredients: ["오이"],
                allergies: [],
                dietary_restrictions: []
            },
            cooking_tools: ["전자레인지"]
        });
        console.log('🌱 초기 테스트 유저 생성 완료');
    }
};
seedUser();

// --- API 라우트 ---

// 1. 내 프로필 조회
app.get('/api/me', async (req, res) => {
    try {
        const user = await User.findOne();
        if (!user) return res.status(404).json({ message: '유저가 없습니다.' });
        res.json(user);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// 2. 내 프로필 수정
app.put('/api/me', async (req, res) => {
    try {
        const user = await User.findOne();
        if (!user) return res.status(404).json({ message: '유저가 없습니다.' });

        const updatedUser = await User.findByIdAndUpdate(
            user._id,
            req.body,
            { new: true, runValidators: true }
        );
        
        console.log('📝 프로필 업데이트:', updatedUser.email);
        res.json(updatedUser);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

app.listen(PORT, () => {
    console.log(`🚀 서버 실행 중: http://localhost:${PORT}`);
});
