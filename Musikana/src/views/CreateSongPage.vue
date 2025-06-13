<template>
	<div class="create-song-page">
		<div class="overlay" v-if="isLoading">
			<p>Processing song generation... Please wait.</p>
		</div>

		<h1>Create a Song</h1>
		<div class="creation-form">
			<!-- Left Panel -->
			<div class="left-panel">
				<div class="box">
					<div class="form-group">
						<label for="title">Title:</label>
						<input type="text" id="title" v-model="title" placeholder="Enter song title" />
					</div>
					<div class="form-group">
						<label for="fanNFTMaxSupply">Fan NFT Max Supply:</label>
						<input type="number" id="fanNFTMaxSupply" v-model="fanNFTMaxSupply" placeholder="Enter fan NFT max supply" />
					</div>
				</div>
				<div class="box">
					<div class="form-group">
						<label for="copyrightNftMaxSupply">Copyright NFT Max Supply:</label>
						<input type="number" id="copyrightNftMaxSupply" v-model="copyrightNftMaxSupply" placeholder="Enter copyright NFT max supply" />
					</div>
					<div class="form-group">
						<label for="copyrightNftPrice">Copyright NFT Price:</label>
						<input type="number" id="copyrightNftPrice" v-model="copyrightNftPrice" placeholder="Enter copyright NFT price" />
					</div>
				</div>

				<div class="form-group">
					<label for="prompt">Prompt:</label>
					<textarea id="prompt" v-model="prompt" rows="5" placeholder="Describe the music you want to create..."></textarea>
				</div>

				<div class="form-group">
					<label for="genre">Genre:</label>
					<select id="genre" v-model="selectedGenre">
						<option v-for="genre in genres" :key="genre.label" :value="genre.value">
							{{ genre.label }}
						</option>
					</select>
				</div>

				<div class="form-group">
					<label for="negative-genre">Negative Genre:</label>
					<select id="negativeGenre" v-model="negativeGenre">
						<option v-for="genre in filteredNegativeGenres" :key="genre.label" :value="genre.value">
							{{ genre.label }}
						</option>
					</select>
				</div>

				<button @click="generateSong" class="generate-button">Generate Song</button>

				<div v-if="error" class="error">{{ error }}</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from "axios";
import { ethers } from "ethers";
import { useRouter } from "vue-router";
import Cookies from "js-cookie";
import { API_URL, GENRES, ADDRESS, songsContractABI } from "@/utils";

export default {
	name: "CreateSongPage",
	setup() {
		const router = useRouter();
		const token = Cookies.get("access_token");
		return {
			router,
			token,
		};
	},
	data() {
		return {
			title: "",
			fanNFTMaxSupply: "",
			copyrightNftMaxSupply: "",
			copyrightNftPrice: "",
			prompt: "",
			selectedGenre: "",
			negativeGenre: "",
			isLoading: false,
			error: null,
			genres: GENRES,

			
			contractAddress: ADDRESS,
			contractABI: songsContractABI,
		};
	},
	computed: {
		filteredNegativeGenres() {
			return this.genres.filter((genre) => genre.value !== this.selectedGenre);
		},
	},
	methods: {
		async generateSong() {
			if (!this.title || !this.prompt || !this.selectedGenre) {
				this.error = "Please fill all required fields.";
				return;
			}

			this.isLoading = true;
			this.error = null;

			try {
				// Step 1: POST /generate
				const generateRes = await axios.post(
					`${API_URL}generate`,
					{
						song_name: this.title,
						prompt: this.prompt,
						styles: [this.selectedGenre],
						negative_styles: [this.negativeGenre],
					},
					{
						headers: {
							Authorization: `Bearer ${this.token}`,
						},
					},
				);

				const taskId = generateRes.data.task_id;
				const uri = `${API_URL}suno/${taskId}`; 

				// aufruf der Smart Contract Function
				if (typeof window.ethereum === "undefined") {
					this.error = "MetaMask not found. Please install it.";
					this.isLoading = false;
					return;
				}

				await window.ethereum.request({ method: "eth_requestAccounts" });
				const provider = new ethers.providers.Web3Provider(window.ethereum);
				const signer = provider.getSigner();

				const songContract = new ethers.Contract(this.contractAddress, this.contractABI, signer);

				const nextSongId = await axios.get(`${API_URL}next_song_id`, {
					headers: {
						Authorization: `Bearer ${this.token}`,
					},
				});

				const tx = await songContract.create_song(
					this.title,
					[this.selectedGenre], // styles as array
					[this.negativeGenre], // negative styles as array
					uri,
					parseInt(this.fanNFTMaxSupply),
					parseInt(this.copyrightNftMaxSupply),
					parseInt(this.copyrightNftPrice),
				);
				this.status = "Transaction sent. Waiting for confirmation...";

				// Wait for transaction to be mined
				await tx.wait();

				await axios.post(
					`${API_URL}create/fan/area`,
					{
						song_id: nextSongId?.data?.[0],
						force_to_create: false,
					},
					{
						headers: {
							Authorization: `Bearer ${this.token}`,
						},
					},
				);

				// wenn es klapt, weiterleiten zu Songs
				this.$router.push("/songs");
			} catch (err) {
				console.error(err);
				this.error = err.response?.data?.message || err.message;
			} finally {
				this.isLoading = false;
			}
		},
	},
};
</script>

<style scoped>
.create-song-page {
	max-width: 900px;
	margin: auto;
}

.creation-form {
	display: flex;
	gap: 30px;
}

.left-panel {
	flex: 1;
}


.form-group {
	width: 100%;
	margin-bottom: 20px;
}

.form-group label {
	display: block;
	margin-bottom: 5px;
	font-weight: bold;
}

.form-group textarea,
.form-group select,
.form-group input[type="text"],
.form-group input[type="number"] {
	width: 100%;
	padding: 10px;
	border: 1px solid #ccc;
	border-radius: 4px;
	box-sizing: border-box;
}

.form-group textarea {
	min-height: 80px;
}

.box {
	display: flex;
	gap: 20px;
	width: 100%;
}

.generate-button {
	padding: 12px 25px;
	background-color: #42b983;
	color: white;
	border: none;
	border-radius: 5px;
	cursor: pointer;
	font-size: 1.1em;
	font-weight: bold;
}

.generate-button:hover {
	background-color: #36a86e;
}

.image-placeholder {
	width: 100%;
	height: 200px;
	background-color: #eee;
	border: 1px dashed #ccc;
	display: flex;
	justify-content: center;
	align-items: center;
	color: #aaa;
	border-radius: 4px;
}

div[v-if] {
	margin-top: 15px;
	font-weight: bold;
}

div[v-if^="error"] {
	color: red;
}

div[v-if^="generatedSongUrl"] {
	color: green;
}

.overlay {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background: rgba(255, 255, 255, 0.8);
	display: flex;
	justify-content: center;
	align-items: center;
	font-size: 1.5em;
	z-index: 999;
}

.error {
	width: 200px;
	color: red;
	margin-top: 10px;
	text-wrap: wrap;
	word-wrap: break-word;
	white-space: pre-wrap;
}
</style>
