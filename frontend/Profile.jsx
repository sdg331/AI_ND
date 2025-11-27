import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { User, Heart, AlertCircle, ChefHat, Settings, LogOut, Plus, Loader2, X, Sparkles } from "lucide-react";

// API 함수들
const fetchUserData = async () => {
    // TODO: 실제 API 호출로 교체
    await new Promise(resolve => setTimeout(resolve, 500));
    return {
        email: "user@example.com",
        cook_goals: "주 3회 직접 요리하기",
        skill_level: "초보",
        preferences: {
            favorite_ingredients: ["계란", "스팸"],
            disliked_ingredients: ["오이"],
            allergies: [],
            dietary_restrictions: []
        },
        cooking_tools: ["프라이팬", "냄비"]
    };
};

const updateUserProfile = async (data) => {
    // TODO: 실제 API 호출로 교체
    await new Promise(resolve => setTimeout(resolve, 1000));
    console.log("Updated Data:", data);
    return data;
};

const logoutUser = async () => {
    // TODO: 실제 로그아웃 로직으로 교체
    console.log("Logged out");
};

const PreferenceSection = ({ title, items, onRemove, onAdd, inputValue, onInputChange, isEditing, placeholder, icon }) => {
    return (
        <div className="space-y-3">
            <Label className="text-sm font-semibold flex items-center gap-2 text-gray-700">
                {icon}
                {title}
            </Label>
            <div className="flex gap-2 flex-wrap min-h-[40px] items-start">
                {items?.length > 0 ? (
                    items.map((item, index) => (
                        <Badge 
                            key={index} 
                            className="bg-amber-100 text-amber-800 hover:bg-amber-200 border-0 px-3 py-1.5 text-sm font-medium transition-colors"
                        >
                            {item}
                            {isEditing && (
                                <button
                                    onClick={() => onRemove(index)}
                                    className="ml-2 hover:opacity-70"
                                >
                                    <X className="w-3.5 h-3.5" />
                                </button>
                            )}
                        </Badge>
                    ))
                ) : (
                    <span className="text-gray-400 text-sm py-1">등록된 항목이 없습니다</span>
                )}
            </div>
            
            {isEditing && (
                <div className="flex gap-2 pt-1">
                    <Input
                        value={inputValue}
                        onChange={onInputChange}
                        onKeyPress={(e) => {
                            if (e.key === "Enter") {
                                e.preventDefault();
                                onAdd();
                            }
                        }}
                        placeholder={placeholder}
                        className="h-10 text-sm border-amber-200 focus:border-amber-400 focus:ring-amber-400"
                    />
                    <Button 
                        onClick={onAdd} 
                        disabled={!inputValue.trim()} 
                        size="sm" 
                        className="bg-amber-500 hover:bg-amber-600 text-white px-4 h-10 shadow-sm"
                    >
                        <Plus className="w-4 h-4" />
                    </Button>
                </div>
            )}
        </div>
    );
};

export default function Profile() {
    const [isEditing, setIsEditing] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [isSaving, setIsSaving] = useState(false);
    const [showToast, setShowToast] = useState({ show: false, message: "", type: "success" });
    const [user, setUser] = useState(null);

    const toast = {
        success: (message) => setShowToast({ show: true, message, type: "success" }),
        error: (message) => setShowToast({ show: true, message, type: "error" }),
        info: (message) => setShowToast({ show: true, message, type: "info" })
    };

    useEffect(() => {
        if (showToast.show) {
            const timer = setTimeout(() => setShowToast({ show: false, message: "", type: "success" }), 3000);
            return () => clearTimeout(timer);
        }
    }, [showToast.show]);

    useEffect(() => {
        const loadUser = async () => {
            try {
                const userData = await fetchUserData();
                setUser(userData);
                setProfileData({
                    cook_goals: userData.cook_goals || "",
                    skill_level: userData.skill_level || "초보",
                    preferences: userData.preferences || {
                        favorite_ingredients: [],
                        disliked_ingredients: [],
                        allergies: [],
                        dietary_restrictions: []
                    },
                    cooking_tools: userData.cooking_tools || []
                });
            } catch (error) {
                console.error("Error loading user:", error);
            } finally {
                setIsLoading(false);
            }
        };
        loadUser();
    }, []);

    const [profileData, setProfileData] = useState({
        cook_goals: "",
        skill_level: "초보",
        preferences: {
            favorite_ingredients: [],
            disliked_ingredients: [],
            allergies: [],
            dietary_restrictions: []
        },
        cooking_tools: []
    });

    const [tempInputs, setTempInputs] = useState({
        favorite: "",
        disliked: "",
        allergy: "",
        dietary: "",
        tool: ""
    });

    const handleAddItem = (inputKey, dataKey, subKey = null) => {
        const value = tempInputs[inputKey].trim();
        if (!value) return;

        let currentList = [];
        if (subKey) {
            currentList = profileData.preferences[subKey] || [];
        } else {
            currentList = profileData[dataKey] || [];
        }

        if (currentList.includes(value)) {
            toast.info(`'${value}'은(는) 이미 등록되어 있습니다`);
            setTempInputs(prev => ({ ...prev, [inputKey]: "" }));
            return;
        }

        setProfileData(prev => {
            if (subKey) {
                return {
                    ...prev,
                    preferences: {
                        ...prev.preferences,
                        [subKey]: [...currentList, value]
                    }
                };
            }
            return {
                ...prev,
                [dataKey]: [...currentList, value]
            };
        });

        setTempInputs(prev => ({ ...prev, [inputKey]: "" }));
    };

    const handleRemoveItem = (dataKey, subKey, index) => {
        setProfileData(prev => {
            if (subKey) {
                return {
                    ...prev,
                    preferences: {
                        ...prev.preferences,
                        [subKey]: prev.preferences[subKey].filter((_, i) => i !== index)
                    }
                };
            }
            return {
                ...prev,
                [dataKey]: prev[dataKey].filter((_, i) => i !== index)
            };
        });
    };

    const handleSave = async () => {
        setIsSaving(true);
        try {
            await updateUserProfile(profileData);
            toast.success("프로필이 업데이트되었습니다!");
            setIsEditing(false);
        } catch (error) {
            toast.error(`업데이트 실패: ${error.message || "오류 발생"}`);
        } finally {
            setIsSaving(false);
        }
    };

    const handleLogout = () => {
        if (window.confirm("정말 로그아웃 하시겠습니까?")) {
            logoutUser();
            toast.success("로그아웃 되었습니다");
        }
    };

    if (isLoading) {
        return (
            <div className="min-h-screen flex flex-col items-center justify-center gap-4 bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50">
                <Loader2 className="w-14 h-14 text-amber-500 animate-spin" />
                <p className="text-gray-600 text-sm font-medium">정보를 불러오는 중...</p>
            </div>
        );
    }

    if (!user) {
        return (
            <div className="min-h-screen flex flex-col items-center justify-center gap-4 bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50">
                <AlertCircle className="w-14 h-14 text-red-500" />
                <p className="text-gray-600 text-sm font-medium">정보를 불러올 수 없습니다</p>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50">
            {showToast.show && (
                <div className={`fixed top-6 left-1/2 transform -translate-x-1/2 z-50 px-6 py-4 rounded-2xl shadow-2xl text-white text-sm font-semibold backdrop-blur-sm ${
                    showToast.type === "success" ? "bg-emerald-500" :
                    showToast.type === "error" ? "bg-rose-500" :
                    "bg-amber-500"
                }`}>
                    {showToast.message}
                </div>
            )}

            {/* Hero Header */}
            <div className="bg-white shadow-sm border-b border-amber-100">
                <div className="max-w-3xl mx-auto px-5 py-8">
                    <div className="flex items-start justify-between">
                        <div className="flex items-start gap-4">
                            <div className="bg-gradient-to-br from-amber-400 to-orange-500 p-4 rounded-2xl shadow-lg">
                                <User className="w-7 h-7 text-white" />
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold text-gray-900 mb-1 flex items-center gap-2">
                                    내 프로필
                                    <Sparkles className="w-5 h-5 text-amber-500" />
                                </h1>
                                <p className="text-sm text-gray-500 font-medium">{user.email}</p>
                            </div>
                        </div>
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={handleLogout}
                            className="border-amber-200 hover:bg-amber-50 text-gray-700 font-medium"
                        >
                            <LogOut className="w-4 h-4 mr-2" />
                            로그아웃
                        </Button>
                    </div>
                </div>
            </div>

            <div className="max-w-3xl mx-auto px-5 py-8 space-y-6">
                {/* 수정/저장 버튼 */}
                <div className="flex justify-end">
                    <Button
                        onClick={() => isEditing ? handleSave() : setIsEditing(true)}
                        disabled={isSaving}
                        className={`font-semibold px-6 py-2.5 rounded-xl shadow-lg transition-all ${
                            isEditing 
                            ? "bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 text-white" 
                            : "bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white"
                        }`}
                    >
                        {isSaving ? (
                            <>
                                <Loader2 className="w-4 h-4 mr-2 animate-spin inline" />
                                저장 중...
                            </>
                        ) : isEditing ? (
                            <>
                                <Sparkles className="w-4 h-4 mr-2 inline" />
                                저장하기
                            </>
                        ) : (
                            <>
                                <Settings className="w-4 h-4 mr-2 inline" />
                                수정하기
                            </>
                        )}
                    </Button>
                </div>

                {/* 기본 정보 카드 */}
                <Card className="border-0 shadow-lg rounded-3xl overflow-hidden bg-white">
                    <CardHeader className="bg-gradient-to-r from-amber-500 to-orange-500 text-white pb-6 pt-6">
                        <CardTitle className="flex items-center gap-3 text-lg font-bold">
                            <div className="bg-white/20 p-2 rounded-xl">
                                <Settings className="w-5 h-5" />
                            </div>
                            기본 정보
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="pt-8 pb-8 px-7 space-y-6">
                        <div>
                            <Label className="text-sm font-semibold mb-3 block text-gray-700">🎯 요리 목표</Label>
                            <Textarea
                                value={profileData.cook_goals}
                                onChange={(e) => setProfileData({ ...profileData, cook_goals: e.target.value })}
                                placeholder="예: 이번 달 배달 음식 줄이기, 건강한 식단 만들기"
                                disabled={!isEditing}
                                className="resize-none min-h-[100px] text-sm border-amber-200 focus:border-amber-400 focus:ring-amber-400 rounded-xl"
                            />
                        </div>
                        <div>
                            <Label className="text-sm font-semibold mb-3 block text-gray-700">👨‍🍳 요리 실력</Label>
                            <div className="grid grid-cols-3 gap-3">
                                {["초보", "중급", "고급"].map((level) => (
                                    <Button
                                        key={level}
                                        type="button"
                                        onClick={() => isEditing && setProfileData({ ...profileData, skill_level: level })}
                                        disabled={!isEditing}
                                        className={`h-12 text-base font-semibold rounded-xl transition-all ${
                                            profileData.skill_level === level 
                                            ? "bg-gradient-to-r from-amber-400 to-orange-500 text-white shadow-lg scale-105" 
                                            : "bg-amber-50 hover:bg-amber-100 border-2 border-amber-200 text-gray-700 shadow-sm"
                                        }`}
                                    >
                                        {level}
                                    </Button>
                                ))}
                            </div>
                        </div>
                    </CardContent>
                </Card>

                {/* 취향 분석 카드 */}
                <Card className="border-0 shadow-lg rounded-3xl overflow-hidden bg-white">
                    <CardHeader className="bg-gradient-to-r from-pink-500 to-rose-500 text-white pb-6 pt-6">
                        <CardTitle className="flex items-center gap-3 text-lg font-bold">
                            <div className="bg-white/20 p-2 rounded-xl">
                                <Heart className="w-5 h-5" />
                            </div>
                            취향 분석
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="pt-8 pb-8 px-7 space-y-8">
                        <PreferenceSection
                            title="좋아하는 재료"
                            icon="💚"
                            items={profileData.preferences.favorite_ingredients}
                            onRemove={(idx) => handleRemoveItem(null, "favorite_ingredients", idx)}
                            onAdd={() => handleAddItem("favorite", null, "favorite_ingredients")}
                            inputValue={tempInputs.favorite}
                            onInputChange={(e) => setTempInputs({ ...tempInputs, favorite: e.target.value })}
                            isEditing={isEditing}
                            placeholder="예: 연어, 아보카도, 토마토"
                        />
                        <div className="border-t border-gray-100"></div>
                        <PreferenceSection
                            title="싫어하는 재료"
                            icon="❌"
                            items={profileData.preferences.disliked_ingredients}
                            onRemove={(idx) => handleRemoveItem(null, "disliked_ingredients", idx)}
                            onAdd={() => handleAddItem("disliked", null, "disliked_ingredients")}
                            inputValue={tempInputs.disliked}
                            onInputChange={(e) => setTempInputs({ ...tempInputs, disliked: e.target.value })}
                            isEditing={isEditing}
                            placeholder="예: 오이, 고수, 파프리카"
                        />
                    </CardContent>
                </Card>

                {/* 건강 & 식단 카드 */}
                <Card className="border-0 shadow-lg rounded-3xl overflow-hidden bg-white">
                    <CardHeader className="bg-gradient-to-r from-emerald-500 to-teal-500 text-white pb-6 pt-6">
                        <CardTitle className="flex items-center gap-3 text-lg font-bold">
                            <div className="bg-white/20 p-2 rounded-xl">
                                <AlertCircle className="w-5 h-5" />
                            </div>
                            건강 & 식단
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="pt-8 pb-8 px-7 space-y-8">
                        <PreferenceSection
                            title="알레르기 정보"
                            icon="⚠️"
                            items={profileData.preferences.allergies}
                            onRemove={(idx) => handleRemoveItem(null, "allergies", idx)}
                            onAdd={() => handleAddItem("allergy", null, "allergies")}
                            inputValue={tempInputs.allergy}
                            onInputChange={(e) => setTempInputs({ ...tempInputs, allergy: e.target.value })}
                            isEditing={isEditing}
                            placeholder="예: 땅콩, 갑각류, 우유"
                        />
                        <div className="border-t border-gray-100"></div>
                        <PreferenceSection
                            title="식단 제한"
                            icon="🥗"
                            items={profileData.preferences.dietary_restrictions}
                            onRemove={(idx) => handleRemoveItem(null, "dietary_restrictions", idx)}
                            onAdd={() => handleAddItem("dietary", null, "dietary_restrictions")}
                            inputValue={tempInputs.dietary}
                            onInputChange={(e) => setTempInputs({ ...tempInputs, dietary: e.target.value })}
                            isEditing={isEditing}
                            placeholder="예: 비건, 키토제닉, 글루텐프리"
                        />
                    </CardContent>
                </Card>

                {/* 조리 도구 카드 */}
                <Card className="border-0 shadow-lg rounded-3xl overflow-hidden bg-white">
                    <CardHeader className="bg-gradient-to-r from-blue-500 to-cyan-500 text-white pb-6 pt-6">
                        <CardTitle className="flex items-center gap-3 text-lg font-bold">
                            <div className="bg-white/20 p-2 rounded-xl">
                                <ChefHat className="w-5 h-5" />
                            </div>
                            보유 조리 도구
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="pt-8 pb-8 px-7">
                        <PreferenceSection
                            title="조리 도구 목록"
                            icon="🔪"
                            items={profileData.cooking_tools}
                            onRemove={(idx) => handleRemoveItem("cooking_tools", null, idx)}
                            onAdd={() => handleAddItem("tool", "cooking_tools")}
                            inputValue={tempInputs.tool}
                            onInputChange={(e) => setTempInputs({ ...tempInputs, tool: e.target.value })}
                            isEditing={isEditing}
                            placeholder="예: 에어프라이어, 믹서기, 오븐"
                        />
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
