<template>
	<div class="my-songs-page">
		<div class="header">
			<h1>My Songs</h1>
			<p id="address">{{ address }}</p>
		</div>
		<p>Here you can manage the NFTs you own (Prototype: includes OWNER_NFTs, Fan NFTs, & Copyright NFTs).</p>

		<div v-if="!hasAccess" class="access-denied">
			<h2><BlockHelperIcon :size="30" />Access Denied</h2>
			<p>Could not load your NFT list. In the full version, please ensure your wallet is connected and try again.</p>
			<button @click="checkAndLoadMyNFTs" class="retry-button">Reload My NFTs ()</button>
		</div>

		<div v-else class="content-area">
			<div class="nft-list">
				<h3>My NFTs</h3>

				<div class="filters">
					<label for="nft-filter">Show:</label>
					<select id="nft-filter" v-model="filterType">
						<option value="all">All NFTs</option>
						<option value="owner_nft">OWNER NFTs</option>
						<option value="fan_nft">FAN NFTs</option>
						<option value="copyright_nft">COPYRIGHT NFTs</option>
					</select>
				</div>

				<p v-if="isLoadingNFTs" class="loading">
					<LoadingIcon class="icon" :size="40" />
				</p>
				<p v-else-if="filteredNFTs.length === 0" class="no-nfts">No NFTs found for this filter.</p>
				<SongCard v-else v-for="nft in filteredNFTs" :key="nft.id" :song="nft" @click="selectNFT(nft)" :class="{ selected: selectedNFT && selectedNFT.song_id === nft.id }" />
			</div>

			<div class="nft-detail-view" v-if="selectedNFT">
				<h2>Details for: {{ selectedNFT.song_name }}</h2>
				<div class="detail-summary">
					<img :src="selectedNFT.image_url || 'https://placehold.co/150?text=No+Cover'" alt="NFT Cover" class="detail-cover" />
					<div class="detail-info">
						<h3>{{ selectedNFT.song_name || "Untitled NFT" }}</h3>
						<p><strong>Type:</strong> {{ formatNFTType(selectedNFT.type) }}</p>
						<p><strong>Genre:</strong> {{ selectedNFT.styles?.[0] || "Unknown" }}</p>
						<p v-if="selectedNFT.artist"><strong>Artist:</strong> {{ selectedNFT.artist }}</p>
						<p class="detail-price" v-if="selectedNFT.price"><strong>Price:</strong> {{ selectedNFT.price }}</p>
						<div class="audio-player-placeholder">
							<audio ref="audioPlayer" @play="playAudio" @pause="pauseAudio" class="audio-player-hidden" controls v-if="selectedNFT.audio_url">
								<source :src="selectedNFT.audio_url" type="audio/mp3" />
								Your browser does not support the audio element.
							</audio>
							<span>Audio Player Placeholder for {{ selectedNFT.song_name }}</span>
							<button @click="playAudio" v-if="!isAudioPlaying">▶ Play</button>
							<button @click="pauseAudio" v-else>⏸ Pause</button>
						</div>
					</div>
				</div>

				<div v-if="selectedNFT.type === 'owner_nft' || selectedNFT.type === 'copyright_nft' || selectedNFT.type === 'fan_nft'" class="management-section">
					<h4>Manage This {{ formatNFTType(selectedNFT.type) }}</h4>
					<p>Owner: You ({{ address }})</p>
					<p>NFT ID: {{ selectedNFT.id || "N/A" }}</p>
					<template v-if="selectedNFT.type === 'owner_nft'">
						<h5>Sales Management</h5>
						<div v-if="!selectedNFT.isForSale">
							<div class="form-group">
								<label for="sell-price">Set Price (e.g., ETH):</label>
								<input type="text" id="sell-price" v-model="sellPrice" placeholder="0.1" />
							</div>
							<button class="sell-button" @click="listForSale(selectedNFT)" :disabled="!sellPrice">List for Sale</button>
						</div>
						<div v-else>
							<p><strong>Currently listed for sale at:</strong> {{ selectedNFT.price }}</p>
							<button class="unlist-button" @click="unlistFromSale(selectedNFT)">Remove from Sale</button>
						</div>
					</template>

					<div v-if="selectedNFT.type === 'owner_nft' || selectedNFT.type === 'copyright_nft' || selectedNFT.type === 'fan_nft'" class="exclusive-content-management">
						<h5>Exclusive Content Management</h5>
						<div class="management-block">
							<h6>Channel Messages</h6>
							<p v-if="selectedNFT.chat?.length">Current Channel Message: {{ selectedNFT.chat?.[0]?.message }}</p>
							<textarea v-if="!selectedNFT.chat?.length" v-model="newChannelMessage" placeholder="Edit exclusive message for this NFT..." rows="3"></textarea>
							<button v-if="!selectedNFT.chat?.length" class="save-button" @click="saveChannelMessages(selectedNFT.song_id)">Save Message</button>
						</div>
						<div class="management-block">
							<h6>Music Video (MV)</h6>
							<p v-if="selectedNFT.mv">Current MV Link: {{ selectedNFT.mv }}</p>
							<input type="text" v-if="!selectedNFT.mv" v-model="newMvLink" placeholder="Link to exclusive MV file..." />
							<button v-if="!selectedNFT.mv" class="save-button" @click="saveMvLink(selectedNFT.song_id)">Save MV Link</button>
						</div>
						<div class="management-block">
							<h6>Remixes</h6>
							<p>Remix List Placeholder:</p>
							<ul>
								<a v-for="remix in selectedNFT.remixs" :key="remix.title" :href="remix.url" target="_blank"><li>{{ remix.title }}</li></a>
							</ul>
							<input type="text" v-model="newRemixLink" placeholder="Link to new remix file..." />
							<button class="save-button" @click="addRemix(selectedNFT.song_id)">Add Remix</button>
						</div>
						<div class="management-block">
							<input type="text" v-model="newOwnerAddress" placeholder="Enter new owner address..." />
							<button class="edit-metadata-button" @click="transferOwnershipNft(selectedNFT)">Edit Owner</button>
						</div>
					</div>
				</div>
			</div>
			<div class="nft-detail-view placeholder" v-else>
				<p>Select one of your NFTs from the list to view details and manage (OWNER_NFTs & Copyright NFTs).</p>
			</div>
		</div>
	</div>
</template>

<script>
import { ref, onMounted, computed } from "vue";
import { ethers } from "ethers";
import axios from "axios";
import Cookies from "js-cookie";
import { API_URL, INFURA_URL, ADDRESS, ABI } from "@/utils";
import LockIcon from "vue-material-design-icons/Lock.vue";
import BlockHelperIcon from "vue-material-design-icons/BlockHelper.vue";
import LoadingIcon from "vue-material-design-icons/Loading.vue";
import SongCard from "@/components/SongCard.vue";

export default {
	name: "MySongsPage",
	components: {
		LockIcon,
		BlockHelperIcon,
		LoadingIcon,
		SongCard,
	},
	data() {
		return {
			newOwnerAddress: "",
			newRemixLink: "",
			newChannelMessage: "",
			newMvLink: "",
			contractABI: ABI,
			infuraUrl: INFURA_URL,
			contractAddress: ADDRESS,
			address: Cookies.get("address"),
		};
	},
	setup() {
		// State Variablen
		const hasAccess = ref(false);
		const isLoadingNFTs = ref(false);
		const allMyNFTs = ref([]);
		const selectedNFT = ref(null);
		const filterType = ref("all");
		const sellPrice = ref("");
		const audioPlayer = ref(null);
		const isLoadingSongDetails = ref(false);
		const isAudioPlaying = ref(false);
		const address = ref(Cookies.get("address"));
		const newOwnerAddress = ref("");
		const infuraUrl = ref(INFURA_URL);
		const contractABI = ref(ABI);
		const contractAddress = ref(ADDRESS);
		const token = ref(Cookies.get("access_token"));
		const newChannelMessage = ref("");
		const newMvLink = ref("");
		const newRemixLink = ref("");

		const filteredNFTs = computed(() => {
			if (filterType.value === "all") {
				return allMyNFTs.value;
			} else {
				return allMyNFTs.value.filter((nft) => nft.type === filterType.value);
			}
		});

		// Formatierung des NFT-Typs für die Anzeige
		const formatNFTType = (type) => {
			switch (type) {
				case "owner_nft":
					return "OWNER_NFT";
				case "fan_nft":
					return "Fan NFT";
				case "copyright_nft":
					return "Copyright NFT";
				default:
					return type;
			}
		};

		// ist Nutzer eingeloggt ?
		async function checkWalletConnection() {
			let walletAddress = Cookies.get("address");
			if (!walletAddress) {
				hasAccess.value = false;
				const provider = new ethers.providers.Web3Provider(window.ethereum);
				await provider.send("eth_requestAccounts", []);
				const signer = provider.getSigner();
				const address = await signer.getAddress();
				Cookies.set("address", address, { expires: 1 });
				walletAddress = address;
			}
			hasAccess.value = true;
			return walletAddress;
		}

		
		async function fetchMyNFTs() {
			const walletAddress = await checkWalletConnection();
			if (!walletAddress) return;

			isLoadingNFTs.value = true;

			try {
				const response = await axios.get(`${API_URL}wallet/${walletAddress}`);

				const processNFTs = async (items, type) => {
					return Promise.all(
						items.map(async (item) => {
							const base = {
								id: item.song_id,
								song_id: item.song_id,
								type: type,
								song_name: item.song_name,
								price: (item.copyright_nft_price / 1000000000).toFixed(8),
								styles: item.styles,
								url: item.uri || "#",
								image_url: null,
							};

							// Fetch image from uri
							try {
								if (item.uri) {
									const metadataResponse = await axios.get(item.uri);
									base.image_url = metadataResponse?.data?.response?.data?.data?.[0]?.image_url || null;
								}
							} catch (err) {
								console.warn(`Could not fetch image for ${item.song_name}`, err);
								base.image_url = null;
							}

							if (type === "owner_nft") {
								return {
									...base,
									price: `${item.copyright_nft_price} ETH`,
									isForSale: !!item.copyright_nft_price,
									fan_nft_maxSupply: item.fan_nft_maxSupply,
									copyright_nft_maxSupply: item.copyright_nft_maxSupply,
									contracts: {
										owner: item.owner_nft_contract,
										fan: item.fan_nft_contract,
										copyright: item.copyright_nft_contract,
									},
								};
							}

							return base;
						}),
					);
				};

				const [ownerNFTs, fanNFTs, copyrightNFTs] = await Promise.all([
					processNFTs(response.data.OWNER_NFT || [], "owner_nft"),
					processNFTs(response.data.FAN_NFT || [], "fan_nft"),
					processNFTs(response.data.COPYRIGHT_NFT || [], "copyright_nft"),
				]);

				allMyNFTs.value = [...ownerNFTs, ...fanNFTs, ...copyrightNFTs];
			} catch (error) {
				console.error("API Error:", error);
				hasAccess.value = false;
				allMyNFTs.value = [];
			} finally {
				isLoadingNFTs.value = false;
			}
		}

		function checkAndLoadMyNFTs() {
			checkWalletConnection().then((walletAddress) => {
				if (walletAddress) {
					fetchMyNFTs();
				}
			});
		}

		async function fetchSongDetails(song) {
			try {
				isLoadingSongDetails.value = true;
				const response = await axios.get(`${song.url}`);
				const fanArea = await axios.get(`${API_URL}get/fan/area/${song.id}`, {
					headers: {
						Authorization: `Bearer ${token.value}`,
					},
				});
				const areaData = fanArea.data;
				const songData = { ...song, ...response?.data?.response?.data?.data?.[0], ...areaData };
				selectedNFT.value = songData;
			} catch (error) {
				console.error("Error fetching song details:", error);
			} finally {
				isLoadingSongDetails.value = false;
			}
		}
		async function selectNFT(nft) {
			await fetchSongDetails(nft);
		}

		async function transferOwnershipNft(nft) {
			if (!nft || !nft.contracts || !nft.contracts.owner) {
				alert("Invalid NFT data. Please select a valid NFT.");
				return;
			}

			if (!newOwnerAddress.value) {
				alert("Please enter a valid new owner address.");
				return;
			}

			try {
				// Request account access if not already granted
				await window.ethereum.request({ method: "eth_requestAccounts" });

				const provider = new ethers.providers.Web3Provider(window.ethereum);
				const signer = provider.getSigner();

				const contract = new ethers.Contract(
					nft.contracts.owner,
					contractABI.value, 
					signer,
				);

				const tx = await contract.transferOwnership(newOwnerAddress.value);

				// Wait for the transaction to be mined
				await tx.wait();
				alert(`Successfully transferred ${nft.song_name} to ${newOwnerAddress.value}`);
				fetchMyNFTs();
				newOwnerAddress.value = "";
				selectedNFT.value = null;
			} catch (error) {
				console.error("Error transferring ownership:", error);
				alert(`Failed to transfer ${nft.song_name}. Check the console for details.`);
			}
		}

		function listForSale(nft) {
			if (!sellPrice.value || isNaN(parseFloat(sellPrice.value))) {
				alert("Please enter a valid price.");
				return;
			}

			const item = allMyNFTs.value.find((i) => i.id === nft.id);
			if (item) {
				item.isForSale = true;
				item.price = `${sellPrice.value} ETH`;
			}
			sellPrice.value = "";
			alert(` ${nft.name} listed for ${item.price}`);
		}

		function unlistFromSale(nft) {
			const item = allMyNFTs.value.find((i) => i.id === nft.id);
			if (item) {
				item.isForSale = false;
				item.price = null;
			}
			alert(` ${nft.name} removed from sale`);
		}

		function playAudio() {
			audioPlayer.value.play();
			isAudioPlaying.value = true;
		}

		function pauseAudio() {
			audioPlayer.value.pause();
			isAudioPlaying.value = false;
		}

		async function saveChannelMessages(nftId) {
			if (!newChannelMessage.value) {
				alert("Please enter a channel message.");
				return;
			}

			try {
				const response = await axios.post(
					`${API_URL}update/fan/area`,
					{
						song_id: nftId,
						remixs: selectedNFT.value.remixs,
						mv: selectedNFT.value.mv,
						chat: [
							...selectedNFT.value.chat,
							{
								sender: Cookies.get("address"),
								message: newChannelMessage.value,
								timestamp: new Date().toISOString(),
							},
						],
					},
					{
						headers: {
							Authorization: `Bearer ${token.value}`,
						},
					},
				);
				alert(` Channel message saved for ${nftId}`);
			} catch (error) {
				console.error("Error saving channel message:", error);
				alert(`Failed to save channel message for ${nftId}. Check the console for details.`);
			}
		}

		async function saveMvLink(nftId) {
			if (!newMvLink.value) {
				alert("Please enter a MV link.");
				return;
			}
			try {
				const response = await axios.post(
					`${API_URL}update/fan/area`,
					{
						song_id: nftId,
						remixs: selectedNFT.value.remixs,
						mv: newMvLink.value,
						chat: selectedNFT.value.chat,
					},
					{
						headers: {
							Authorization: `Bearer ${token.value}`,
						},
					},
				);
				alert(`: MV link saved for ${nftId}`);
			} catch (error) {
				console.error("Error saving MV link:", error);
				alert(`Failed to save MV link for ${nftId}. Check the console for details.`);
			}
		}

		async function addRemix(nftId) {
			if (!newRemixLink.value) {
				alert("Please enter a remix link.");
				return;
			}

			try {
				const response = await axios.post(
					`${API_URL}update/fan/area`,
					{
						song_id: nftId,
						remixs: [
							...selectedNFT.value.remixs,
							{
								url: newRemixLink.value,
								title: `My Remix ${selectedNFT.value.remixs.length + 1}`,
							},
						],
						mv: selectedNFT.value.mv,
						chat: selectedNFT.value.chat,
					},
					{
						headers: {
							Authorization: `Bearer ${token.value}`,
						},
					},
				);
				alert(`: Remix added for ${nftId}`);
			} catch (error) {
				console.error("Error adding remix:", error);
				alert(`Failed to add remix for ${nftId}. Check the console for details.`);
			}
		}

		// Lifecycle Hook
		onMounted(() => {
			checkAndLoadMyNFTs();
		});

		return {
			audioPlayer,
			isAudioPlaying,
			hasAccess,
			isLoadingNFTs,
			filteredNFTs,
			selectedNFT,
			filterType,
			sellPrice,
			formatNFTType,
			selectNFT,
			listForSale,
			unlistFromSale,
			playAudio,
			pauseAudio,
			address,
			transferOwnershipNft,
			newOwnerAddress,
			newChannelMessage,
			newMvLink,
			newRemixLink,
			saveChannelMessages,
			saveMvLink,
			addRemix,
		};
	},
};
</script>

<style scoped>

.my-songs-page {
	max-width: 1200px;
	margin: 20px auto;
	padding: 20px;
	background-color: var(--color-background);
	color: var(--color-text);
}

.my-songs-page .header {
	color: var(--color-primary);
	border-bottom: 1px solid var(--color-primary-hover);
	padding-bottom: 10px;
	margin-bottom: 20px;
	display: flex;
	align-items: center;
	justify-content: space-between;
}
.my-songs-page .header h1 {
	color: var(--color-primary);
}

.my-songs-page > p {
	color: var(--color-primary-hover);
	margin-bottom: 20px;
}

.content-area {
	display: flex;
	gap: 30px;
	min-height: 500px;
}

.nft-list .filters {
	margin-bottom: 15px;
	padding-bottom: 15px;
	border-bottom: 1px solid #444;
	display: flex;
	align-items: center;
	gap: 10px;
}

.nft-list .filters label {
	font-weight: bold;
	color: #f2f2f2;
	font-size: 0.9em;
}

.nft-list .filters select {
	padding: 5px 8px;
	border-radius: 4px;
	border: 1px solid #ccc;
	background-color: #666;
	color: white;
	font-size: 0.9em;
}

.nft-detail-view h2 {
	color: var(--color-primary);
}

.no-nfts {
	color: #aaa;
	font-style: italic;
}

.detail-summary .detail-info p.detail-price {
	font-weight: bold;
	color: var(--color-primary);
	font-size: 1em;
}

.management-and-content-sections {
	display: flex;
	flex-direction: column;
	gap: 20px;
}

.management-section {
	border: 1px solid #444;
	border-radius: 8px;
	padding: 15px;
	background-color: #666;
	color: #f2f2f2;
}

.management-section h4 {
	margin-top: 0;
	margin-bottom: 15px;
	color: #f2f2f2;
	border-bottom: 1px solid #555;
	padding-bottom: 8px;
}

.management-section p {
	margin: 5px 0;
	font-size: 0.9em;
	color: #ccc;
}

.management-section .form-group {
	margin: 10px 0;
}

.management-section .form-group label {
	display: block;
	font-size: 0.8em;
	margin-bottom: 3px;
	color: #ccc;
}

.management-section .form-group input[type="text"] {
	padding: 5px 8px;
	border-radius: 4px;
	border: 1px solid #ccc;
	background-color: #777;
	color: white;
	width: 100px;
}

.management-section button {
	padding: 8px 15px;
	border: none;
	border-radius: 5px;
	cursor: pointer;
	font-weight: bold;
	margin-right: 10px;
	margin-top: 5px;
}

.exclusive-content-management {
	border: 1px solid #444;
	border-radius: 8px;
	padding: 15px;
	background-color: #666;
	color: #f2f2f2;
}

.exclusive-content-management h5 {
	margin-top: 0;
	margin-bottom: 15px;
	color: #f2f2f2;
	border-bottom: 1px solid #555;
	padding-bottom: 8px;
}

.exclusive-content-management .management-block {
	margin-bottom: 20px;
	padding-bottom: 15px;
	border-bottom: 1px dashed #555;
}

.exclusive-content-management .management-block:last-child {
	border-bottom: none;
	padding-bottom: 0;
	margin-bottom: 0;
}

.exclusive-content-management .management-block h6 {
	margin-top: 0;
	margin-bottom: 10px;
	color: #ccc;
	font-size: 1em;
}

.exclusive-content-management textarea,
.exclusive-content-management input[type="text"] {
	width: 100%;
	padding: 8px;
	border-radius: 4px;
	border: 1px solid #ccc;
	background-color: #777;
	color: white;
	box-sizing: border-box;
	margin-bottom: 10px;
}

.exclusive-content-management textarea {
	min-height: 80px;
	resize: vertical;
}

.exclusive-content-management button {
	padding: 8px 15px;
	border: none;
	border-radius: 5px;
	cursor: pointer;
	font-weight: bold;
	margin-right: 10px;
	margin-top: 5px;
}

.exclusive-content-management ul {
	list-style: none;
	padding: 0;
	margin-bottom: 15px;
}

.exclusive-content-management li {
	background-color: #777;
	padding: 8px 12px;
	border-radius: 4px;
	margin-bottom: 8px;
	display: flex;
	justify-content: space-between;
	align-items: center;
}

@media (max-width: 768px) {
	.content-area {
		flex-direction: column;
		gap: 20px;
	}

	.nft-list .filters {
		justify-content: center;
		flex-wrap: wrap;
	}

	.nft-detail-view {
		flex: auto;
	}

	.detail-summary {
		flex-direction: column;
		align-items: center;
		text-align: center;
	}

	.detail-summary .detail-info p {
		text-align: left;
	}

	.management-section button,
	.exclusive-content-management button {
		margin-right: 5px;
		margin-bottom: 5px;
	}

	.exclusive-content-management li button {
		margin-right: 0;
		margin-bottom: 0;
	}
}
</style>
