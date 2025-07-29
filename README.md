# Google_ADK_Agentic_Simulatiton_product_recommendation

## Overview:
- Recommend agent recommends products and image url of products.
-  When user hits query, it checks for its capabilities and leverages tools associated with to query Vertex AI search and retrieves product name and url.
-  Data store is created based on data pushed to google cloud storage. 
- It passed evaluation with evalset created with adk ui for tool trajectory score and response matching score.

## Demo :

https://github.com/user-attachments/assets/a6d501bb-04d2-48a2-b6b2-88c5429428e7


## Dataset used:
- clothing, shoe and jewelry dataset
- https://amazon-reviews-2023.github.io/

## Technologies Used
- Google Agent Development Kit
- gemini-2.0-flash (Gemini API)
- Vertex AI Search
- Vertex AI data store
- RAG
- Google cloud storage
