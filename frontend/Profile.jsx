import React, { useState, useEffect } from "react";
// import { base44 } from "@/api/base44Client"; 
import { 
    useQuery, 
    useMutation, 
    useQueryClient, 
    QueryClient, 
    QueryClientProvider 
} from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { User as UserIcon, Heart, AlertCircle, ChefHat, Settings, LogOut, Plus, Loader2 } from "lucide-react";
import { toast } from "sonner";
import { useNavigate, BrowserRouter } from "react-router-dom";

/**
 * [API Mock Object]
 * 실제 프로젝트에서는 api/base44Client.js로 분리하여 사용합니다.
 */
const base44 = {
    auth: {
        me: async () => {
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
        },
        updateMe: async (data) => {
            await new Promise(resolve => setTimeout(resolve, 1000));
            console.log("Updated Data:", data);
            return data;
        },
        logout: async () => {
            console.log("Logged out");
        }
    }
};

// React Query Client 생성
const queryClient = new QueryClient();

/**
 * [Helper Component] PreferenceSection
 */
const PreferenceSection = ({ title, items, onRemove, onAdd, inputValue, onInputChange, isEditing, placeholder, colorTheme = "green" }) => {
    const colorClasses = {
        green: "bg-green-100 text-green-800 hover:bg-green-200",
        red: "bg-red-100 text-red-800 hover:bg-red-200",
        yellow: "bg-yellow-100 text-yellow-800 hover:bg-yellow-200", // orange -> yellow로 변경하여 사용 가능
        purple: "bg-purple-100 text-purple-800 hover:bg-purple-200",
    };

    return (
        <div className="mb-4">
            <Label className="text-base font-semibold flex items-center gap-2 mb-2">
                {title}
            </Label>
            <div className="flex gap-2 mb-3 flex-wrap min-h-[32px] items-center">
                {items?.length > 0 ? (
                    items.map((item, index) => (
                        <Badge key={index} className={`${colorClasses[colorTheme] || colorClasses.green} transition-colors`}>
                            {item}
                            {isEditing && (
                                <button
                                    onClick={() => onRemove(index)}
                                    className="ml-2 hover:opacity-70 focus:outline-none"
                                    aria-label={`${item} 삭제`}
                                >
                                    &times;
                                </button>
                            )}
                        </Badge>
                    ))
                ) : (
                    <span className="text-gray-400 text-sm">등록된 항목이 없습니다.</span>
                )}
            </div>
            
            {isEditing && (
                <div className="flex gap-2 max-w-sm">
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
                        className="h-9 focus-visible:ring-yellow-400"
                    />
                    <Button onClick={onAdd} disabled={!inputValue.trim()} size="sm" className="bg-yellow-500 hover:bg-yellow-600 text-white">
                        <Plus className="w-4 h-4" />
                    </Button>
                </div>
            )}
        </div>
    );
};

/**
 * [Component] CookingToolsSection
 */
const CookingToolsSection = ({ tools, isEditing, inputValue, setInputValue, onAdd, onRemove }) => {
    return (
        <Card className="border-yellow-200 shadow-md">
            <CardHeader>
                <CardTitle className="flex items-center gap-2">
                    <ChefHat className="w-5 h-5 text-yellow-600" />
                    보유 조리 도구
                </CardTitle>
            </CardHeader>
            <CardContent>
                <div className="flex gap-2 mb-4 flex-wrap min-h-[40px] items-center">
                    {tools && tools.length > 0 ? (
                        tools.map((item, index) => (
                            <Badge key={index} className="bg-blue-100 text-blue-800 hover:bg-blue-200 transition-colors px-3 py-1">
                                {item}
                                {isEditing && (
                                    <button
                                        onClick={() => onRemove(index)}
                                        className="ml-2 hover:text-blue-900 focus:outline-none font-bold"
                                        aria-label={`${item} 제거`}
                                    >
                                        &times;
                                    </button>
                                )}
                            </Badge>
                        ))
                    ) : (
                        <p className="text-gray-500 text-sm">
                            등록된 조리 도구가 없습니다. 레시피 추천 정확도를 위해 추가해주세요!
                        </p>
                    )}
                </div>
                
                {isEditing && (
                    <div className="flex gap-2">
                        <Input
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyPress={(e) => {
                                if (e.key === "Enter") {
                                    e.preventDefault();
                                    onAdd();
                                }
                            }}
                            placeholder="예: 에어프라이어, 믹서기, 오븐"
                            className="max-w-xs focus-visible:ring-yellow-400"
                        />
                        <Button 
                            onClick={onAdd}
                            disabled={!inputValue.trim()}
                            className="bg-yellow-500 hover:bg-yellow-600 text-white"
                        >
                            <Plus className="w-4 h-4 mr-1" /> 추가
                        </Button>
                    </div>
                )}
            </CardContent>
        </Card>
    );
};

/**
 * [Internal Component] ProfileContent
 */
function ProfileContent() {
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    
    const [isEditing, setIsEditing] = useState(false);

    const { data: user, isLoading, isError } = useQuery({
        queryKey: ["user"],
        queryFn: () => base44.auth.me(),
        retry: 1,
    });

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

    useEffect(() => {
        if (user) {
            setProfileData({
                cook_goals: user.cook_goals || "",
                skill_level: user.skill_level || "초보",
                preferences: user.preferences || {
                    favorite_ingredients: [],
                    disliked_ingredients: [],
                    allergies: [],
                    dietary_restrictions: []
                },
                cooking_tools: user.cooking_tools || []
            });
        }
    }, [user]);

    const updateProfileMutation = useMutation({
        mutationFn: (data) => base44.auth.updateMe(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["user"] });
            toast.success("프로필이 성공적으로 업데이트되었습니다!");
            setIsEditing(false);
        },
        onError: (error) => {
            toast.error(`업데이트 실패: ${error.message || "알 수 없는 오류가 발생했습니다."}`);
        }
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
            toast.info(`'${value}'(은)는 이미 등록되어 있습니다.`);
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

    const handleSave = () => {
        updateProfileMutation.mutate(profileData);
    };

    const handleLogout = () => {
        if (window.confirm("정말 로그아웃 하시겠습니까?")) {
            base44.auth.logout();
            toast.success("로그아웃 되었습니다.");
        }
    };

    if (isLoading) {
        return (
            <div className="min-h-screen flex flex-col items-center justify-center gap-4">
                <Loader2 className="w-10 h-10 text-yellow-500 animate-spin" />
                <p className="text-gray-500">사용자 정보를 불러오는 중...</p>
            </div>
        );
    }

    if (isError || !user) {
        return (
            <div className="min-h-screen flex flex-col items-center justify-center gap-4">
                <AlertCircle className="w-10 h-10 text-red-500" />
                <p className="text-gray-500">정보를 불러올 수 없습니다. 다시 로그인해주세요.</p>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-yellow-50/30 pb-10">
            {/* Header Section - 노란색 테마 적용 (Yellow to Orange Gradient) */}
            <div className="bg-gradient-to-r from-yellow-400 to-orange-400 text-white p-8 shadow-lg">
                <div className="max-w-4xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
                    <div className="flex items-center gap-4">
                        <div className="bg-white/30 p-3 rounded-full">
                            <UserIcon className="w-8 h-8 text-white" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold text-white drop-shadow-sm">내 프로필</h1>
                            <p className="text-yellow-50 font-medium">{user.email}</p>
                        </div>
                    </div>
                    <Button
                        variant="ghost"
                        className="text-white hover:bg-white/20 border border-transparent hover:border-white/30"
                        onClick={handleLogout}
                    >
                        <LogOut className="w-4 h-4 mr-2" />
                        로그아웃
                    </Button>
                </div>
            </div>

            <div className="max-w-4xl mx-auto px-4 -mt-6 space-y-6">
                {/* 1. 기본 정보 카드 */}
                <Card className="shadow-lg border-none">
                    <CardHeader className="flex flex-row items-center justify-between border-b pb-4">
                        <CardTitle className="flex items-center gap-2 text-xl">
                            <Settings className="w-6 h-6 text-yellow-500" />
                            기본 정보 설정
                        </CardTitle>
                        <Button
                            variant={isEditing ? "default" : "outline"}
                            onClick={() => isEditing ? handleSave() : setIsEditing(true)}
                            disabled={updateProfileMutation.isPending}
                            className={`min-w-[80px] ${isEditing ? "bg-yellow-500 hover:bg-yellow-600 text-white border-transparent" : "border-yellow-200 hover:bg-yellow-50 text-yellow-700"}`}
                        >
                            {updateProfileMutation.isPending ? (
                                <Loader2 className="w-4 h-4 animate-spin" />
                            ) : isEditing ? (
                                "저장 완료"
                            ) : (
                                "프로필 수정"
                            )}
                        </Button>
                    </CardHeader>
                    <CardContent className="pt-6 space-y-6">
                        <div>
                            <Label htmlFor="cook_goals" className="text-base mb-2 block">요리 목표</Label>
                            <Textarea
                                id="cook_goals"
                                value={profileData.cook_goals}
                                onChange={(e) => setProfileData({ ...profileData, cook_goals: e.target.value })}
                                placeholder="예: 이번 달에는 배달 음식 줄이기"
                                disabled={!isEditing}
                                className="resize-none min-h-[80px] text-base focus-visible:ring-yellow-400"
                            />
                        </div>
                        <div>
                            <Label className="text-base mb-2 block">현재 요리 실력</Label>
                            <div className="flex gap-3">
                                {["초보", "중급", "고급"].map((level) => (
                                    <Button
                                        key={level}
                                        type="button"
                                        variant={profileData.skill_level === level ? "default" : "outline"}
                                        onClick={() => isEditing && setProfileData({ ...profileData, skill_level: level })}
                                        disabled={!isEditing}
                                        className={`flex-1 h-12 text-lg transition-all ${
                                            profileData.skill_level === level 
                                            ? "bg-yellow-400 hover:bg-yellow-500 text-white ring-2 ring-yellow-200 border-transparent font-bold shadow-sm" 
                                            : "hover:bg-yellow-50 border-gray-200 text-gray-600"
                                        }`}
                                    >
                                        {level}
                                    </Button>
                                ))}
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <div className="grid md:grid-cols-2 gap-6">
                    {/* 2. 음식 선호도 */}
                    <Card className="shadow-md border-yellow-100">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <Heart className="w-5 h-5 text-red-400" />
                                취향 분석
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <PreferenceSection
                                title="좋아하는 재료 💚"
                                items={profileData.preferences.favorite_ingredients}
                                onRemove={(idx) => handleRemoveItem(null, "favorite_ingredients", idx)}
                                onAdd={() => handleAddItem("favorite", null, "favorite_ingredients")}
                                inputValue={tempInputs.favorite}
                                onInputChange={(e) => setTempInputs({ ...tempInputs, favorite: e.target.value })}
                                isEditing={isEditing}
                                placeholder="예: 연어, 아보카도"
                                colorTheme="green"
                            />
                            <div className="my-4 border-t border-gray-100" />
                            <PreferenceSection
                                title="싫어하는 재료 ❌"
                                items={profileData.preferences.disliked_ingredients}
                                onRemove={(idx) => handleRemoveItem(null, "disliked_ingredients", idx)}
                                onAdd={() => handleAddItem("disliked", null, "disliked_ingredients")}
                                inputValue={tempInputs.disliked}
                                onInputChange={(e) => setTempInputs({ ...tempInputs, disliked: e.target.value })}
                                isEditing={isEditing}
                                placeholder="예: 오이, 고수"
                                colorTheme="red"
                            />
                        </CardContent>
                    </Card>

                    {/* 3. 건강 정보 */}
                    <Card className="shadow-md border-yellow-100">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <AlertCircle className="w-5 h-5 text-amber-500" />
                                건강 & 식단
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                             <PreferenceSection
                                title="알레르기 정보 ⚠️"
                                items={profileData.preferences.allergies}
                                onRemove={(idx) => handleRemoveItem(null, "allergies", idx)}
                                onAdd={() => handleAddItem("allergy", null, "allergies")}
                                inputValue={tempInputs.allergy}
                                onInputChange={(e) => setTempInputs({ ...tempInputs, allergy: e.target.value })}
                                isEditing={isEditing}
                                placeholder="예: 땅콩, 갑각류"
                                colorTheme="yellow" 
                            />
                            <div className="my-4 border-t border-gray-100" />
                            <PreferenceSection
                                title="식단 제한 🥗"
                                items={profileData.preferences.dietary_restrictions}
                                onRemove={(idx) => handleRemoveItem(null, "dietary_restrictions", idx)}
                                onAdd={() => handleAddItem("dietary", null, "dietary_restrictions")}
                                inputValue={tempInputs.dietary}
                                onInputChange={(e) => setTempInputs({ ...tempInputs, dietary: e.target.value })}
                                isEditing={isEditing}
                                placeholder="예: 비건, 키토제닉"
                                colorTheme="purple"
                            />
                        </CardContent>
                    </Card>
                </div>

                {/* 4. 조리 도구 */}
                <CookingToolsSection
                    tools={profileData.cooking_tools}
                    isEditing={isEditing}
                    inputValue={tempInputs.tool}
                    setInputValue={(val) => setTempInputs({ ...tempInputs, tool: val })}
                    onAdd={() => handleAddItem("tool", "cooking_tools")}
                    onRemove={(idx) => handleRemoveItem("cooking_tools", null, idx)}
                />
            </div>
        </div>
    );
}

/**
 * [Export Component]
 * App Wrapper
 */
export default function Profile() {
    return (
        <QueryClientProvider client={queryClient}>
            <BrowserRouter>
                <ProfileContent />
            </BrowserRouter>
        </QueryClientProvider>
    );
}
