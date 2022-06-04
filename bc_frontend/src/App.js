import './App.css';
import Layout from './Layout';
import Home from './Home';
import { Route, Routes, useNavigate } from 'react-router-dom';

function App() {
    return (
        <div className="App">
            <Routes>
                <Route path="/" element={<Layout />}>
                    <Route index element={<Home />} />
                </Route>
            </Routes>
        </div>
    );
}

export default App;
