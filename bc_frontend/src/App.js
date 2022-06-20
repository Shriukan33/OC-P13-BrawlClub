import './App.css';
import Layout from './common/Layout';
import Home from './home/Home';
import Player from './player/Player';
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
