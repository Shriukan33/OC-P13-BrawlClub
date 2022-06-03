import './App.css';
import Nav from './Nav';
import { Route, Routes, useNavigate } from 'react-router-dom';

function App() {
    return (
        <div className="App">
            <Routes>
                <Route path="/*" element={<Nav />} />
            </Routes>
        </div>
    );
}

export default App;
