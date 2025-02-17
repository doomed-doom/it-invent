import { Navigate } from "react-router-dom";

import Login from "../pages/Login/Login";
import Error from "../pages/Error/Error";
import Assets from "../pages/Assets/Assets";

export const publicRoutes = [
	{ path: "/login", element: <Login /> },
	{ path: "*", element: <Navigate to="/login" replace /> },
];

export const privateRoutes = [
	{ path: "/assets/:key", element: <Assets /> },

	{ path: "/login", element: <Navigate to="/assets/equipments" replace /> },
	{ path: "/assets", element: <Navigate to="/assets/equipments" replace /> },
	{ path: "/", element: <Navigate to="/assets/equipments" replace /> },

	{ path: "/error", element: <Error /> },
	{ path: "*", element: <Navigate to="/error" replace /> },
];
