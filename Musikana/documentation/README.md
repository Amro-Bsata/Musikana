# Musikana: An AI-Powered, Blockchain-Enabled Music Platform

## Introduction

The digital age has dramatically reshaped the music industry, offering new avenues for both artists and consumers. Artificial Intelligence (AI) empowers individuals to create music without formal training, yet this bureaucratization complicates issues of copyright and ownership. Traditional legal frameworks often struggle to address AI-generated content adequately. Concurrently, blockchain technology promises to revolutionize the ownership, licensing, and distribution of digital assets. This project, Musikana, aims to bridge these disruptive technologies, creating a platform where AI-generated music can be securely registered, licensed, and enjoyed.

The name "Musikana" itself reflects this innovative union. It combines "Musik" (German for music) with the Arabic suffix "-na," meaning "our music."  Additionally, the name's similarity to "Arcana" hints at the technological mysteries and innovative solutions powering the platform. 

Musikana directly tackles the critical challenges that arise from the convergence of AI and music:

*   **Tokenize the Copyright :** Making selling/buying the Song-Copyright very easy using NFTs.
*   **Ownership Verification:**  Establishing verifiable, blockchain-backed ownership for AI-created compositions. 
*   **Fan Engagement Gaps:** Existing music ecosystems often fail to provide meaningful avenues for fans to support creators directly.
*   **Gated Access:** Secure and decentralized methods for managing access to exclusive content are a core objective.

## Implementation

Musikana's architecture integrates diverse technologies, requiring precise synchronization between its components. To clarify this complex system I use UML diagrams.

### System Design

Musikana employs a client-server architecture. The core components include:

#### Technology Stack

*   **Frontend:** A user-friendly interface developed with Vue.js.
*   **Backend:** A Python server utilizing Flask handles API requests, user authentication, communication with the Suno AI API for music generation, and interaction with the blockchain and MongoDB database.
*   **Smart Contracts:** Solidity contracts deployed on an EVM-compatible blockchain (Sepolia testnet) manage song ownership, NFT minting, and licensing, also storing crucial song data.
*   **Data Storage:** MongoDB is used to store metadata (URIs linking to song files and NFT artwork) and Fan Area content (remixes, chat logs, music video URLs).
*   **MetaMask:** MetaMask provides a secure interface for users to log in, interact with smart contracts, and authorize transactions.

#### Pages

1.  **Homepage:** This is the landing page. It provides a general overview of the platform's features and a button to start creating music.

2.  **Create Song Page:** This page provides the interface for generating music.
    *   **Input Fields:** Users input the song title, a descriptive prompt to guide the AI's composition, and select a genre and a "negative genre" (a genre to avoid).
    *   **NFT Configuration:** Users configure the maximum supply for both Fan NFTs and Copyright NFTs, setting the price for the Copyright NFTs in Gwei (the smallest unit of Ether).

3.  **Songs Page:** The Songs Page is where you can see each Song which has the platform.
    *   **Copyright-nftprice:** you can find on which price the rights for the song are up for to sell.
    *   **Contracts:** In Contracts can you see the Smart Contracts.
    *   **Image and Sound:** Shows you the sound and the Photocover from the song
    *  The backend system gets with the songs together the picture that belongs to it, thats what makes it easier
    * All Songs can be filtered from the specific genres and the system supports pagination

4.  **Marketplace Page:** This section showcases Copyright NFTs for sale, allowing users to purchase music licences.
    *   **Song Listings:**  Displays a list of available songs, including key information like the song title, and the price of the Copyright NFT.
    *   **Search and Filter:** Users can search for specific songs or filter by genre and price.

5.  **My Songs Page:** A dashboard designed for users to manage their owned NFTs and fan content.
    *   **NFT List:** Shows a list of NFTs owned by the user, categorized into OWNER\_NFTs, FAN\_NFTs, and COPYRIGHT\_NFTs.
    *   **NFT Details:** Clicking on an NFT displays comprehensive information, including the song name, metadata, and ownership details.
    *   **Content Management (Fan Area):** Owners of OWNER\_NFTs have the ability to manage exclusive content for their fans, including setting channel messages, uploading music videos, and adding remixes.
        *   **Channel message**: Set a specific message that can only be be reached, by the community that owns the speciffic Fannft.
         *   **Remixes:** Set Remix-Urls for remixes of the song
          *   **Mvs**: Upload the link the Music-Videos

6.  **Top Secrets Page:**
This has some very similar Part to the "My songs " View the diffrence is , that
the use only can be entered by the owener of the specific fannfts, and also it shows only and exactly the content that is related to the fannft.
 *   **Specific Content for Fan-Nft-Users**
* The Users are identified when they connect there Account and the System loads the fanNFTs for it only and makes sure that all content here is specific related only to the fannfts.

## Scenarios


### Generate a Song and Mint Owner NFT

This scenario outlines the process of creating a new song on the platform. The user initiates the process by entering song information (title, Fan NFT max supply, Copyright NFT price, prompt, genre, negative genre) into the frontend application.

*     (please see the Activity Diagram "UML_SONG_GENERATION" for better understanding)

1.  **Frontend sends music info to API:** The frontend sends a `generate_music` request to the backend system with the provided music information.

2.  **Backend Check Payload:** The backend system validates the payload (checking prompt length and other parameters).

3.  **AI API integration:** The backend system communicates with the Musikgenerierungs-KI (Music AI), sending only the necessary information.

4.  **Task creation and sending back to frontEnd:** The Music AI generates the song and returns a `Task_ID` to the backend, which is then passed back to the frontend.
    *   The client uses this ID to create the URI.

5.  **Retrieve next_song_id:** Before interacting with the smart contract, the frontend sends a request to the backend, asking for the `next_song_id`. The backend:
    *   Calls the `get_next_song_id` function in the smart contract using the RPC API.
    *   Returns the `next_song_id` value to the frontend.

6.  **Smart Contract Interaction:** Now, the frontend calls the `create_song` function on the smart contract:
    *   This prompts the user's MetaMask wallet to request a transaction signature.
    *   Upon approval, the smart contract performs the following operations:

        1.  Creates and deploys three NFT collections: OWNER NFT, FAN NFT, and COPYRIGHT NFT.
        2.  Associates the song metadata (including the URI) with the newly created NFTs.

7.  **Fan Area Creation:** Following successful contract interaction, the frontend requests the creation of a "Fan Area" through the backend, using the `song_id` as an identifier.
    *   This function creates a fan-area documentation in mongoDB, which provides the structure for remixes, chat and videos.

8.  **Asynchronous Song Delivery:** Asynchronously, the MusikKI (Music-AI) delivers the generated `Song.mp3/Song.png` files to the backend system via a callback. The backend subsequently updates the state by storing the file locations in the database and associates the songs/photos with the URI. The `Task_ID` creates a link to these files.

## Web3 Authentication

This scenario describes how users authenticate to Musikana using MetaMask (Etherium Wallet).
*     (please see the Activity Diagram "UML_LOGIN" for better understanding)

The user starts the login process by clicking "Login with MetaMask" on the frontend. The frontend then requests the user's wallet address using `eth_requestAccounts` from MetaMask. Upon user approval, MetaMask provides the account address.

The frontend sends a request to the `/api/nonce` endpoint of the backend, including the user's wallet address. The backend generates a unique nonce (number used once) associated with that address and sends it back to the frontend.

The frontend prompts the user to sign the generated nonce with their MetaMask wallet, confirming ownership of the address. After the user signs the message (nonce), the frontend sends the address and signature to the backend for verification. The backend checks if the signature is valid and that the nonce matches the user address.

If the signature is valid, the backend generates a JWT (JSON Web Token) for the user and sends it back to the frontend.

The frontend stores the JWT in a cookie for subsequent authentication and sets a flag to indicate the user is authenticated. This JWT will then be sent back with each API request to prove that the user has successfully authenticated.



## Visiting the My Songs Page
This scenario details the steps when a user navigates to their "My Songs" page, displaying all the NFTs/songs they own.
*     (please see the Activity Diagram "UML_GET_NFTS_PER_WALLET" for better understanding)

**Prerequisites:**

*   The user has successfully authenticated with their MetaMask wallet.

**Steps:**

1.  **User Navigates to "My Songs":**

    *    The user, through their browser, navigates to the "My Songs".

2.  **Frontend Initiates the Request:**

    *    The Vue.js frontend application sends an HTTP `GET` request to the `/wallet/<owner>` endpoint of the Flask API. `<owner>` is replaced with the Ethereum address stored in the user's browser cookies (set during authentication).

3.  **Flask API (Backend) Processes the Request:**

    *    The API receives the `GET` request and prepares to gather the user data.
    *    Flask's routing mechanism directs the request to a specific function (e.g., a `get_nfts_per_owner` function in the `main.py` file).

4.  **Initializing Result JSON:**

    *    `Backend -> Backend: result= {"OWNER_NFT":[],"FAN_NFT":[],"COPYRIGHT_NFT":[]}`
    *    The API initializes a JSON called `result` that contains the keys "OWNER\_NFT", "FAN\_NFT", and "COPYRIGHT\_NFT", each initialized as an empty list `[]`. This JSON will store the categorized NFT data.

5.  **API Queries Moralis API:**

    *    The `Backend` sends a request to the Moralis API to get the NFTs owned by the specified `owner`. The call is `evm_api.nft.get_wallet_nfts(owner)` with parameters including `address`

    *
        
        *   Moralis is a blockchain data provider, streamlining the retrieval of blockchain data.

6.  **Moralis API Responds with NFT Data:**

    *    Moralis --> Backend : `nft_list_response`
    *    The Moralis API returns a JSON response containing a list of NFTs owned by the address. This response includes information about each NFT, such as its contract address (`token_address`), and token ID.

7.  **Looping Through NFTs (Start of `loop`):**

    *    The `Backend` begins iterating through each `nft` returned in the `nft_list_response["result"]`.
    *    A Python `for` loop is used to process each NFT individually.

8.  **Obtain Checksum Address:**

    *    The `Backend` converts the `nft["token_address"]` (which might be in a mixed-case format) to a checksummed address using Web3.py's `w3.to_checksum_address()`.
   

9.  **Determine The Song ID Per NFT smart Contract:**

    *    The `Backend` calls the `Util` function, `get_song_id_per_contract`, to retrieve the Song ID from the NFT Smart Contract.
        *   `Util` establishes an ABI call to the Smart Contract and executes the `song_id().call()` function.
    *    The Python code uses a utility function to retrieve the `song_id` from the NFT smart contract using Web3.py library functions. An RPC call is made to an Ethereum node to query the contract.

10. **Recursive Call to Retrieve Song Information:**

    *     The Backend gets again called 'Backend -> Util : get_song_per_id(song_id)'
    *    The function will return details, if exist for a specific Song-Id.

11. **Extract Relevant Information (if applicable):**

    *    The Backend gets back the information about it and attaches it to the result with the help from the function `deserialize_song(song_data_raw)`.
    *    The function is now returning for the User all the wanted Information about it.

12. **Append Song Object:**

    *    `Backend -> Backend : result[nft_type].append(deserialized_song)`
    *    The deserialized song object (containing information about the song) is appended to the appropriate list within the `result` object ("OWNER\_NFT", "FAN\_NFT", or "COPYRIGHT\_NFT").  The categorization is based on the symbol defined in the ABIs.

13. **Return final Data (After the Loop):**

    *    Backend --> Client : `HTTP 200 OK (result)`
    *    Once the loop completes, the Flask API sends an `HTTP 200 OK` response back to the client. The response body contains the `result` JSON, which contains three lists of songs owned by user, each with the according NFT collection type.

## Conclusion and Outlook
Musikana represents a compelling synthesis of AI and blockchain, providing a novel solution for music creation and ownership in the digital age. By leveraging AI for music generation and blockchain technology for NFT-based ownership and licensing, the platform addresses critical challenges surrounding copyright and provenance in the rapidly evolving digital landscape. Through detailed exploration of use cases such as song creation, user authentication, and access management, the project demonstrates the capabilities and potential of a fully integrated system.

However, the practical implementation highlighted some constraints. The reliance on fetching data directly from the blockchain resulted in slow response times, impacting the user experience. To mitigate this, an alternative data solution was developed and implemented as part of the "Weiterführende Konzepte in Datenbanken" course, significantly improving website speed by approximately 1000x. 