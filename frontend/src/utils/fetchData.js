import axios from "axios";
import Cookies from "js-cookie";

export const refreshTokens = async () => {
	const refresh = Cookies.get("refresh");

	if (!refresh) return console.warn("Refresh token отсутствует!") || false;

	try {
		const { data } = await axios.post(
			"http://localhost:8000/api/auth/token/",
			{ refresh }
		);

		Cookies.set("access", data.access, {
			expires: 15 / 1440,
			// secure: true,
			sameSite: "Lax",
		});
		Cookies.set("refresh", data.refresh, {
			expires: 30,
			// secure: true,
			sameSite: "Lax",
		});

		window.location.reload();

		return true;
	} catch (err) {
		return false;
	}
};

export const fetchData = async (
    url,
    method,
    data = null,
    setResponse = null,
    setFetchError = null,
    setFetchSuccess = null,
    isFileDownload = false,
    fileName = "download.csv"
) => {

    let access = Cookies.get("access");

    try {
        const response = await axios({
            method,
            url: `http://localhost:8000/api/${url}/`,
            data,
            headers: {
                Authorization: `Bearer ${access}`,
                ...(data instanceof FormData ? {} : { "Content-Type": "application/json" })
            },
            responseType: isFileDownload ? "blob" : "json",
        });

        console.log("Успех:", response.data);

		if (response.data.access && response.data.refresh) {
			Cookies.set("access", response.data.access, {
				expires: 15 / 1440,
				// secure: true,
				sameSite: "Lax",
			});
			Cookies.set("refresh", response.data.refresh, {
				expires: 30,
				// secure: true,
				sameSite: "Lax",
			});
			window.location.reload();
		}

		setResponse?.(response.data);
		setFetchSuccess?.(response.data.message);

        if (isFileDownload) {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const a = document.createElement("a");
            a.href = url;
            a.download = fileName;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        } else {
            setResponse?.(response.data);
            setFetchSuccess?.(response.data.message);
        }
    } catch (error) {
		if (error.response) {
			const fetchError = error.response.data.detail;
			console.error("Ошибка ответа:", error.response.data);
			setFetchError?.(fetchError || "Ошибка сервера.");

			if (
				fetchError === "Authentication credentials were not provided."
			) {
				console.warn("Токен истёк. Попытка обновить токен...");

				await refreshTokens();
			}
		} else {
			console.error("Ошибка сети или сервера:", error.message);
			setFetchError?.("Ошибка сети или сервера.");
		}
	}
};
