const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
    email: { 
        type: String, 
        required: true, 
        unique: true,
        trim: true 
    },
    cook_goals: { 
        type: String, 
        default: "" 
    },
    skill_level: { 
        type: String, 
        enum: ['초보', '중급', '고급'], 
        default: '초보' 
    },
    preferences: {
        favorite_ingredients: [String],   // 좋아하는 재료
        disliked_ingredients: [String],   // 싫어하는 재료
        allergies: [String],              // 알레르기
        dietary_restrictions: [String]    // 식단 제한
    },
    cooking_tools: [String]               // 조리 도구
}, { 
    timestamps: true 
});

module.exports = mongoose.model('User', UserSchema);
