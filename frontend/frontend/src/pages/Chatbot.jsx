    import React, { useState, useEffect, useRef } from "react";
    import {
    MessageCircle,
    Send,
    RotateCcw,
    Brain,
    CheckCircle,
    } from "lucide-react";

    const MChatChatbot = () => {
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [progress, setProgress] = useState("0/10");
    const [isComplete, setIsComplete] = useState(false);
    const [sessionId] = useState(() => `session_${Date.now()}`);
    const messagesEndRef = useRef(null);

    const API_URL = import.meta.env.VITE_API_URL;

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        startConversation();
    }, []);

    const startConversation = async () => {
        setIsLoading(true);
        try {
        const response = await fetch(`${API_URL}/start`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: sessionId }),
        });
        const data = await response.json();
        setMessages([{ role: "assistant", content: data.message }]);
        setProgress(data.progress);
        setIsComplete(false);
        } catch (error) {
        console.error("Error starting conversation:", error);
        setMessages([
            {
            role: "assistant",
            content:
                "Hello! I'm here to help you complete the M-CHAT screening questionnaire. Are you ready to begin? (yes/no)",
            },
        ]);
        } finally {
        setIsLoading(false);
        }
    };

    const sendMessage = async () => {
        if (!inputValue.trim() || isLoading) return;

        const userMessage = inputValue.trim();
        setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
        setInputValue("");
        setIsLoading(true);

        try {
        const response = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
            session_id: sessionId,
            message: userMessage,
            }),
        });
        const data = await response.json();

        setTimeout(() => {
            setMessages((prev) => [
            ...prev,
            { role: "assistant", content: data.message },
            ]);
            setProgress(data.progress || "0/10");
            setIsComplete(data.isComplete || false);
            setIsLoading(false);
        }, 500);
        } catch (error) {
        console.error("Error sending message:", error);
        setMessages((prev) => [
            ...prev,
            {
            role: "assistant",
            content:
                "Sorry, there was an error. Please make sure the Flask server is running on port 5000.",
            },
        ]);
        setIsLoading(false);
        }
    };

    const handleReset = async () => {
        setIsLoading(true);
        try {
        const response = await fetch(`${API_URL}/reset`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: sessionId }),
        });
        const data = await response.json();
        setMessages([{ role: "assistant", content: data.message }]);
        setProgress(data.progress);
        setIsComplete(false);
        } catch (error) {
        console.error("Error resetting:", error);
        startConversation();
        } finally {
        setIsLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
        }
    };

    const handleQuickReply = (reply) => {
        setInputValue(reply);
        setTimeout(() => sendMessage(), 100);
    };

    return (
        <div className="min-h-screen bg-linear-to-r from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4">
        <div
            className="w-full max-w-4xl bg-white rounded-2xl shadow-2xl overflow-hidden flex flex-col"
            style={{ height: "90vh" }}
        >
            {/* Header */}
            <div className="bg-linear-to-r from-indigo-600 to-purple-600 text-white p-6 shadow-lg">
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                <div className="bg-white/20 p-3 rounded-lg backdrop-blur-sm">
                    <Brain className="w-8 h-8" />
                </div>
                <div>
                    <h1 className="text-2xl font-bold">M-CHAT Screening Tool</h1>
                    <p className="text-indigo-100 text-sm">
                    Autism Spectrum Disorder Assessment
                    </p>
                </div>
                </div>
                <button
                onClick={handleReset}
                className="bg-white/20 hover:bg-white/30 p-2 rounded-lg transition-colors backdrop-blur-sm"
                id="resetBut"
                title="Start New Assessment"
                >
                <RotateCcw className="w-7 h-7" />
                </button>
            </div>

            {/* Progress Bar */}
            <div className="mt-4">
                <div className="flex justify-between text-sm mb-2">
                <span>Progress</span>
                <span className="font-semibold">{progress}</span>
                </div>
                <div className="w-full bg-white/20 rounded-full h-2 backdrop-blur-sm">
                <div
                    className="bg-white h-2 rounded-full transition-all duration-500 ease-out"
                    style={{
                    width: progress.includes("/")
                        ? `${(parseInt(progress.split("/")[0]) / 10) * 100}%`
                        : isComplete
                        ? "100%"
                        : "0%",
                    }}
                />
                </div>
            </div>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50">
            {messages.map((msg, index) => (
                <div
                key={index}
                className={`flex ${
                    msg.role === "user" ? "justify-end" : "justify-start"
                } animate-fadeIn`}
                >
                <div
                    className={`max-w-[75%] rounded-2xl px-5 py-3 shadow-md ${
                    msg.role === "user"
                        ? "bg-linear-to-r from-indigo-600 to-purple-600 text-white rounded-br-sm"
                        : "bg-white text-gray-800 rounded-bl-sm border border-gray-200"
                    }`}
                >
                    {msg.role === "assistant" && (
                    <div className="flex items-center gap-2 mb-2 text-indigo-600">
                        <MessageCircle className="w-4 h-4" />
                        <span className="text-xs font-semibold">Assistant</span>
                    </div>
                    )}
                    <p className="whitespace-pre-line leading-relaxed">
                    {msg.content}
                    </p>
                    {msg.role === "assistant" &&
                    isComplete &&
                    index === messages.length - 1 && (
                        <div className="mt-3 pt-3 border-t border-gray-200">
                        <div className="flex items-center gap-2 text-green-600">
                            <CheckCircle className="w-5 h-5" />
                            <span className="text-sm font-semibold">
                            Assessment Complete
                            </span>
                        </div>
                        </div>
                    )}
                </div>
                </div>
            ))}

            {isLoading && (
                <div className="flex justify-start animate-fadeIn">
                <div className="bg-white rounded-2xl px-5 py-3 shadow-md border border-gray-200">
                    <div className="flex items-center gap-2">
                    <div className="flex space-x-1">
                        <div
                        className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce"
                        style={{ animationDelay: "0ms" }}
                        />
                        <div
                        className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce"
                        style={{ animationDelay: "150ms" }}
                        />
                        <div
                        className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce"
                        style={{ animationDelay: "300ms" }}
                        />
                    </div>
                    <span className="text-sm text-gray-500">Typing...</span>
                    </div>
                </div>
                </div>
            )}
            <div ref={messagesEndRef} />
            </div>

            {/* Quick Reply Buttons */}
            {!isComplete && messages.length > 0 && (
            <div className="px-6 py-3 bg-white border-t border-gray-200">
                <div className="flex gap-2 flex-wrap">
                <button
                    onClick={() => handleQuickReply("yes")}
                    className="px-4 py-2 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors text-sm font-medium"
                >
                    Yes
                </button>
                <button
                    onClick={() => handleQuickReply("no")}
                    className="px-4 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors text-sm font-medium"
                >
                    No
                </button>
                </div>
            </div>
            )}

            {/* Input Area */}
            <div className="p-6 bg-white border-t border-gray-200">
            {isComplete ? (
                <button
                onClick={handleReset}
                className="w-full bg-linear-to-r from-indigo-600 to-purple-600 text-white py-3 rounded-xl font-semibold hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg flex items-center justify-center gap-2"
                >
                <RotateCcw className="w-5 h-5" />
                Start New Assessment
                </button>
            ) : (
                <div className="flex gap-3">
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Type your response..."
                    disabled={isLoading}
                    className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all disabled:bg-gray-100"
                />
                <button
                    onClick={sendMessage}
                    disabled={!inputValue.trim() || isLoading}
                    className="bg-linear-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-xl font-semibold hover:from-indigo-700 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg flex items-center gap-2"
                >
                    <Send className="w-5 h-5" />
                    Send
                </button>
                </div>
            )}
            </div>
        </div>

        <style jsx>{`
            @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
            }
            .animate-fadeIn {
            animation: fadeIn 0.3s ease-out;
            }
            #resetBut{
                background-color: #A55DEE;
            }
        `}</style>
        </div>
    );
    };

    export default MChatChatbot;