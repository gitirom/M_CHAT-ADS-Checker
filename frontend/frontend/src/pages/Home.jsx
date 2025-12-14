import { useNavigate } from "react-router-dom";
import { Brain } from "lucide-react";

const Home = () => {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50 flex items-center justify-center">
        <div className="bg-white p-10 rounded-2xl shadow-xl max-w-xl text-center">
            <div className="flex justify-center mb-6">
            <div className="bg-indigo-600 p-4 rounded-xl text-white">
                <Brain size={40} />
            </div>
            </div>

            <h1 className="text-3xl font-bold mb-4">
            M-CHAT Autism Screening Tool
            </h1>

            <p className="text-gray-600 mb-8">
            This tool helps assess the risk of Autism Spectrum Disorder in young
            children using the official M-CHAT questionnaire.
            </p>

            <button
            onClick={() => navigate("/chatbot")}
            className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-8 py-3 rounded-xl font-semibold hover:scale-105 transition"
            >
            Start Screening
            </button>
        </div>
        </div>
    );
};


export default Home;