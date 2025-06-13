<template>
	<div v-if="isLoadingSongDetails" class="loading">
		<BxLoaderCircle class="icon" />
	</div>
	<div class="song-detail-view" v-if="selectedNFT">
		<h2>Song Details for {{ selectedNFT.song_name }}</h2>

		<SongDetail :song="selectedNFT" context="marketplace" />

		<div class="nft-info">
			<h4>Song Information</h4>
			<p><strong>Contract:</strong> {{ selectedNFT.owner_nft_contract || "N/A" }}</p>

			<a v-if="selectedNFT.nftLink" :href="selectedNFT.nftLink" target="_blank"> View on Explorer </a>
		</div>
		<div class="nft-buttons">
			<button class="mint-button" v-if="isFanNFT" @click="mintNFT(selectedNFT)">Mint Fan NFT</button>
		</div>
	</div>

	<div class="song-detail-view placeholder" v-else>
		<p>Select a song from the list to see details.</p>
	</div>
</template>

<script>
import axios from "axios";
import { ethers } from "ethers";
import Cookies from "js-cookie";
import SongDetail from "@/components/SongDetail.vue";
import { CUSTOM_URL, API_URL, ADDRESS, INFURA_URL ,copyrightNFTContractABI} from "@/utils";
import { BxLoaderCircle } from "@kalimahapps/vue-icons";

export default {
	name: "SongDetails",
	components: {
		SongDetail,
		BxLoaderCircle,
	},

	data() {
		return {
			songId: null,
			contractAddress: ADDRESS, 
			contractABI: copyrightNFTContractABI,
			mintTokenPrice: "0.01",
			mintContractABI: [
				{
					inputs: [],
					name: "mintToken",
					outputs: [],
					stateMutability: "nonpayable",
					type: "function",
				},
			],
			address: Cookies.get("address"),
			isLoadingSongDetails: false,
			isFanNFT: false,
			selectedNFT: null,
		};
	},
	watch: {
		// Watch for changes in route (e.g., when user navigates between different song IDs)
		"$route.params.songId": {
			immediate: true,
			handler(newSongId) {
				// SCHUTZPRÜFUNG: Führe nichts aus, wenn keine ID vorhanden ist.
				if (!newSongId) {
					this.selectedNFT = null; // Setze den Zustand zurück, falls die ID entfernt wird
					return; 
				}
				
				this.songId = newSongId;
				this.fetchSongDetails(newSongId);
			},
		},
	},
methods: {
		async fetchSongDetails(songId) {
			try {
				this.isLoadingSongDetails = true;
				const songResponse = await axios.get(`${API_URL}song/${songId}`);
				const songResponseData = songResponse.data;
				const response = await axios.get(songResponseData.uri);
				const fanNFTResponse = await axios.get(`${API_URL}fannft/remaining/${songResponseData.song_id}`);
				this.isFanNFT = fanNFTResponse.data;
				const apiResponse = response?.data?.response?.data?.data?.[0];
				const songData = {
					...songResponseData,
					...(apiResponse || {}),
					price: (songResponseData.copyright_nft_price / 1000000000).toFixed(8),
				};
				this.selectedNFT = songData;
			} catch (error) {
				console.error("Error fetching song details:", error);
			} finally {
				this.isLoadingSongDetails = false;
			}
		},


		async mintNFT(song) {
			console.log(song)
			if (!window.ethereum) {
				this.status = "Please install MetaMask!";
				return;
			}

			const provider = new ethers.providers.Web3Provider(window.ethereum);
			const signer = provider.getSigner();

			try {
				await window.ethereum.request({ method: "eth_requestAccounts" });
				const contract = new ethers.Contract(song.fan_nft_contract, this.mintContractABI, signer);

				const code = await provider.getCode(song.fan_nft_contract);
				if (code === "0x") throw new Error("Contract does not exist");

				const tx = await contract.mintToken({ gasLimit: 300000 });
				await tx.wait();
				alert(`Successfully minted ${song.song_name}`);
			} catch (error) {
				console.error("Error minting NFT:", error);
				alert("Failed to mint NFT. Please check the console for details.");
			}
		},
	},


};
</script>

<style scoped>
.nft-info {
	margin-top: 20px;
	padding-top: 15px;
	border-top: 1px solid #eee;
}

.nft-info h4 {
	margin-bottom: 10px;
}

.nft-info p {
	margin: 5px 0;
	font-size: 0.9em;
}

.nft-info a {
	color: #42b983;
	text-decoration: underline;
}

.nft-buttons {
	display: flex;
	gap: 15px;
}
</style>
