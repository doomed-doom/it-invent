import React, { useEffect, useState } from "react";
import { Navigate, Route, Routes, useParams } from "react-router-dom";
import Cookies from "js-cookie";

import { refreshTokens } from "../utils/fetchData";
import { privateRoutes, publicRoutes } from "../router";
import { fetchData } from "../utils/fetchData";

import NavAssets from "./NavAssets/NavAssets";
import Assets from "../pages/Assets/Assets";
import Loader from "./UI/Loader/Loader";

import classes from "../pages/Page.module.css";

const AssetWrapper = ({ keys }) => {
	const { key } = useParams();
	return keys.includes(key) ? <Assets keys={key}/> : <Navigate to="/error" replace />;
};

const AppRouter = () => {
	const access = Cookies.get("access");
	const refresh = Cookies.get("refresh");

	const [data, setData] = useState(null);

	useEffect(() => {
		if (!access) {
			if (refresh) {
				refreshTokens();
			}
		}

		fetchData("assets", "get", null, setData);
	}, []);

	const keys = data ? Object.keys(data) : [];

	return access ? (
		keys[0] ? (
			<div className={classes.page}>
				<NavAssets tabs={keys} />

				<Routes>
					{privateRoutes.map((route) => (
						<Route
							key={route.path}
							path={route.path}
							element={
								route.path === "/assets/:key" ? (
									<AssetWrapper keys={keys} />
								) : (
									route.element
								)
							}
						/>
					))}
				</Routes>
			</div>
		) : (
			<div className={classes.loader}>
				<Loader />
			</div>
		)
	) : (
		<Routes>
			{publicRoutes.map((route) => (
				<Route
					key={route.path}
					path={route.path}
					element={route.element}
				/>
			))}
		</Routes>
	);
};

export default AppRouter;