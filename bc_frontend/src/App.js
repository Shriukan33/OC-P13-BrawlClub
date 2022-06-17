import './App.css';
import Layout from './Layout';
import Home from './Home';
import Player from './Player';
import { Route, Routes } from 'react-router-dom';
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
    return (
        <>
            <Routes>
                <Route path="/" element={<Layout />}>
                    <Route index element={<Home />} />
                    <Route path="player">
                        <Route index path=":id" element={<Player />} />
                    </Route>
                </Route>
            </Routes>
        </>
    );
}

export default App;
