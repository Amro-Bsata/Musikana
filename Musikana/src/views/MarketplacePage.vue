<template>
	<div class="marketplace-page">
		<h1>Song Marketplace</h1>

		<!-- Search & Filter Controls -->
		<div class="controls">
			<input type="text" v-model="searchTerm" placeholder="Search Song Name or NFT Link..." />

			<select v-model="priceFilter">
				<option value="">All Prices</option>
				<option value="low">Low to High</option>
				<option value="high">High to Low</option>
			</select>
		</div>

		<!-- Main Content -->
		<div class="content-area">
			<!-- Song List -->
			<div class="song-list">
				<p v-if="loading" class="loading">
					<BxLoaderCircle class="icon" />
				</p>

				<p v-else-if="filteredSongs.length === 0">No songs found matching your criteria.</p>

				<SongCard v-else v-for="song in filteredSongs" :key="song.id" :song="song" @click="selectSong(song)" :class="{ selected: selectedSong && selectedSong.id === song.id }" />
			</div>

			<!-- Song Details -->
			<div class="song-detail-view" v-if="selectedNFT">
				<h2>Song Details for {{ selectedNFT.song_name }}</h2>

				<SongDetail :song="selectedNFT" context="marketplace" />

				<div class="nft-info">
					<h4>Song Information</h4>
					<p><strong>Contract:</strong> {{ selectedNFT.nftContract || "N/A" }}</p>
					<p><strong>Type:</strong> {{ selectedNFT.nftType || "Copyright-NFT" }}</p>

					<a v-if="selectedNFT.nftLink" :href="selectedNFT.nftLink" target="_blank"> View on Explorer </a>
				</div>
				<!-- der Song-owner braucht den Buy-Knopf gar nicht -->
				<div class="nft-buttons">
					<button class="buy-button" v-if="address !== selectedNFT.owner" @click="buyNFT(selectedNFT)">Buy Copyright NFT ({{ selectedNFT.price || "Price N/A" }})</button>
				</div>
			</div>

			<!-- Placeholder , wenn kein Lied ausgewählt -->
			<div class="song-detail-view placeholder" v-else>
				<p>Select a song from the list to see details.</p>
			</div>
		</div>
	</div>
</template>

<script>
import axios from "axios";
import { ethers } from "ethers";
import Cookies from "js-cookie";
import SongCard from "@/components/SongCard.vue";
import SongDetail from "@/components/SongDetail.vue";
import { API_URL, ADDRESS, INFURA_URL,copyrightNFTContractABI } from "@/utils";
import { BxLoaderCircle } from "@kalimahapps/vue-icons";

export default {
	name: "MarketplacePage",
	components: {
		SongCard,
		SongDetail,
		BxLoaderCircle,
	},
	data() {
  return {
    loading: false,
    error: null,
    contractAddress: ADDRESS, 
    contractABI: copyrightNFTContractABI,
    address: Cookies.get("address"),
    searchTerm: "",
    priceFilter: "",
    allSongs: [],
    selectedSong: null,
    selectedNFT: null,
    isLoadingSongDetails: false,
    isFanNFT: false,
  };
},

	computed: {
		filteredSongs() {
			let songs = [...this.allSongs];

			if (this.searchTerm) {
				const lowerSearch = this.searchTerm.toLowerCase();
				songs = songs.filter((song) => song.song_name.toLowerCase().includes(lowerSearch) || (song.nftLink && song.nftLink.toLowerCase().includes(lowerSearch)));
			}

			if (this.priceFilter === "low") {
				songs.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
			} else if (this.priceFilter === "high") {
				songs.sort((a, b) => parseFloat(b.price) - parseFloat(a.price));
			}

			return songs;
		},
	},

	methods: {
		async fetchSongs() {
			this.loading = true;
			try {
				const response = await axios.get(`${API_URL}market/songs`);

			
				const songsWithImages = await Promise.all(
					response.data.map(async (song) => {
						let image = null;

						try {
							if (song.uri) {
								const meta = await axios.get(song.uri);
								image = meta?.data?.response?.data?.data?.[0]?.image_url || null;
							}
						} catch (err) {
							console.warn(`Failed to fetch image for song ${song.song_name}`, err);
						}

						return {
							id: song.song_id,
							song_name: song.song_name,
							styles: song.styles || "Unknown",
							price: (song.copyright_nft_price / 1000000000).toFixed(8),
							nftId: song.song_id,
							nftContract: song.copyright_nft_contract,
							nftLink: song.uri,
							nftType: "Copyright-NFT",
							owner: song.owner,
							owner_nft_contract: song.owner_nft_contract,
							url: song.uri,
							image_url: image,
						};
					}),
				);

				this.allSongs = songsWithImages;
			} catch (error) {
				console.error("Error fetching songs:", error);
			} finally {
				this.loading = false;
			}
		},

		async fetchSongDetails(song) {
			if (!song.url) return;

			try {
				this.isLoadingSongDetails = true;
				const response = await axios.get(song.url);
				const fanNFTResponse = await axios.get(`${API_URL}fannft/remaining/${song.id}`);
				this.isFanNFT = fanNFTResponse.data;
				const apiResponse = response?.data?.response?.data?.data?.[0];
				const songData = {
					...song,
					...(apiResponse || {}),
				};
				this.selectedNFT = songData;
			} catch (error) {
				console.error("Error fetching song details:", error);
			} finally {
				this.isLoadingSongDetails = false;
			}
		},

		async selectSong(song) {
			this.selectedSong = song;
			await this.fetchSongDetails(song);
		},

		async buyNFT(song) {
			// Infura configuration
			const infuraUrl = INFURA_URL;
			const provider = new ethers.providers.JsonRpcProvider(infuraUrl);

			try {
				const contract = new ethers.Contract(song.nftContract, this.contractABI, provider);

				const code = await provider.getCode(song.nftContract);
				if (code === "0x") {
					throw new Error("No contract deployed at the given address.");
				}

				let price;
				try {
					price = await contract.price();
				} catch (error) {
					price = ethers.utils.parseEther("0.01"); // Default price
				}

				if (!window.ethereum) {
					alert("MetaMask is required to sign transactions.");
					return;
				}

				const walletProvider = new ethers.providers.Web3Provider(window.ethereum);
				await walletProvider.send("eth_requestAccounts", []);
				const signer = walletProvider.getSigner();

				const signedContract = new ethers.Contract(song.nftContract, this.contractABI, signer);

				const tx = await signedContract.mintToken(signer.getAddress(), { value: price });
				await tx.wait();
				alert(`Successfully purchased ${song.song_name}`);
			} catch (error) {
				console.error("Error buying NFT:", error);
				alert("Failed to purchase NFT. Please check the console for details.");
			}
		},
	},

	created() {
		this.fetchSongs();
	},
};
</script>

<style scoped>
.marketplace-page {
	padding-bottom: 50px;
	
}

.controls {
	display: flex;
	gap: 15px;
	margin-bottom: 25px;
	padding: 15px;
	background-color: #555;
	border-radius: 8px;
}

.controls input[type="text"] {
	flex-grow: 1;
	padding: 8px 12px;
	border: 1px solid #ccc;
	border-radius: 4px;
}

.controls select,
.controls button {
	padding: 8px 15px;
	border: 1px solid #ccc;
	border-radius: 4px;
	background-color: white;
	cursor: pointer;
}

.controls button {
	background-color: #42b983;
	color: white;
	border-color: #42b983;
}

.controls button:hover {
	background-color: #36a86e;
}

.content-area {
	display: flex;
	gap: 30px;
}

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
