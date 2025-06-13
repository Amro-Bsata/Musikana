<template>
	<button v-if="!isAuthenticated" @click="login" class="cta-button" :disabled="loading">
		<span v-if="loading" class="loading-nfts">
			<LoadingIcon class="icon" :size="8" />
		</span>
		<span v-else>Login with MetaMask</span>
	</button>
</template>

<script>
import { ethers } from "ethers";
import axios from "axios";
import Cookies from "js-cookie";
import { API_URL } from "@/utils";
import LoadingIcon from "vue-material-design-icons/Loading.vue";

export default {
	name: "MetaMaskLogin",
	components: {
		LoadingIcon,
	},
	data() {
		return {
			loading: false,
			isAuthenticated: false,
		};
	},
	mounted() {
		const token = Cookies.get("access_token");
		if (token) {
			this.isAuthenticated = true;
		}
	},
	methods: {
		async login() {
			if (!window.ethereum) {
				alert("Please install MetaMask!");
				return;
			}

			this.loading = true;

			try {
				const provider = new ethers.providers.Web3Provider(window.ethereum);
				await provider.send("eth_requestAccounts", []);
				const signer = provider.getSigner();
				const address = await signer.getAddress();

				// 1. Fetch nonce from backend
				const { data } = await axios.get(`${API_URL}/api/nonce`, {
					params: { address },
				});

				// 2. Sign the nonce
				const signature = await signer.signMessage(data.nonce);

				// 3. Send signature to server for verification
				const resp = await axios.post(`${API_URL}/api/login`, {
					address,
					signature,
				});

				if (resp.data.success) {
					const token = resp.data.access_token;
					Cookies.set("access_token", token, { expires: 1 }); // expires in 1 day
					Cookies.set("address", address, { expires: 1 });
					this.isAuthenticated = true;
				} else {
					console.error("Authentication failed:", resp.data.error);
				}
			} catch (error) {
				console.error("Login error:", error.message || error);
			} finally {
				this.loading = false;
			}
		},

		async fetchProtectedData() {
			const token = Cookies.get("access_token");
			if (!token) {
				console.error("No access token found!");
				return;
			}

			try {
				const response = await axios.get(`${API_URL}/protected`, {
					headers: {
						Authorization: `Bearer ${token}`,
					},
				});
			} catch (error) {
				console.error("Access denied or error:", error.response?.data || error.message);
			}
		},
	},
};
</script>
