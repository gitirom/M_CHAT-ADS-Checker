import {Route, Routes} from 'react-router-dom'
import Home from './pages/Home'
import Chatbot from './pages/Chatbot'
import './App.css'

function App() {

  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/chatbot" element={<Chatbot />} />
    </Routes>
  )
}

export default App
