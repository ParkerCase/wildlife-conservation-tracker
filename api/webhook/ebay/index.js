// eBay Webhook Handler
// This endpoint handles various eBay marketplace notifications

export default async function handler(req, res) {
  // Only allow POST requests
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    // Log the incoming webhook for debugging
    console.log("eBay Webhook received:", {
      timestamp: new Date().toISOString(),
      headers: req.headers,
      body: req.body,
    });

    // Extract webhook data
    const webhookData = req.body;

    // Validate webhook data structure
    if (!webhookData || typeof webhookData !== "object") {
      console.error("Invalid webhook data received");
      return res.status(400).json({ error: "Invalid webhook data" });
    }

    // Determine the type of webhook and process accordingly
    const result = await processWebhook(webhookData);

    // Return success response (eBay expects 200 status)
    return res.status(200).json({
      status: "success",
      message: "Webhook processed successfully",
      timestamp: new Date().toISOString(),
      data: result,
    });
  } catch (error) {
    console.error("Error processing eBay webhook:", error);

    // Return 500 error for internal server errors
    return res.status(500).json({
      error: "Internal server error",
      message: error.message,
      timestamp: new Date().toISOString(),
    });
  }
}

async function processWebhook(webhookData) {
  const {
    metadata,
    data,
    eventId,
    eventDate,
    publishDate,
    publishAttemptCount,
    topic,
  } = webhookData;

  // Log the webhook event
  console.log("Processing webhook:", {
    eventId,
    eventDate,
    publishDate,
    publishAttemptCount,
    topic,
    metadata,
    data,
  });

  // Process based on topic/event type
  switch (topic) {
    case "MARKETPLACE_ACCOUNT_DELETION":
    case "MARKETPLACE_ACCOUNT_CLOSURE":
      return await processAccountDeletion(webhookData);

    case "ITEM_SOLD":
      return await processItemSold(webhookData);

    case "ITEM_UPDATED":
      return await processItemUpdated(webhookData);

    case "ITEM_ENDED":
      return await processItemEnded(webhookData);

    default:
      // Handle unknown topics
      console.log("Unknown webhook topic:", topic);
      return {
        processed: true,
        eventId,
        eventDate,
        topic,
        message: "Unknown topic - logged for review",
        processedAt: new Date().toISOString(),
      };
  }
}

async function processAccountDeletion(webhookData) {
  const { data, eventId, eventDate } = webhookData;

  console.log("Processing account deletion:", {
    eventId,
    eventDate,
    accountInfo: data?.accountInfo || {},
    deletionReason: data?.deletionReason || "Unknown",
  });

  // Here you can add your custom logic for handling account deletions
  // For example:
  // - Update your database to mark the account as deleted
  // - Stop monitoring this account
  // - Send notifications to your team
  // - Archive any relevant data

  return {
    processed: true,
    eventId,
    eventDate,
    accountInfo: data?.accountInfo || {},
    deletionReason: data?.deletionReason || "Unknown",
    processedAt: new Date().toISOString(),
  };
}

async function processItemSold(webhookData) {
  const { data, eventId, eventDate } = webhookData;

  console.log("Processing item sold:", {
    eventId,
    eventDate,
    itemId: data?.itemId,
    sellerId: data?.sellerId,
  });

  // Handle item sold events
  return {
    processed: true,
    eventId,
    eventDate,
    itemId: data?.itemId,
    sellerId: data?.sellerId,
    processedAt: new Date().toISOString(),
  };
}

async function processItemUpdated(webhookData) {
  const { data, eventId, eventDate } = webhookData;

  console.log("Processing item updated:", {
    eventId,
    eventDate,
    itemId: data?.itemId,
    sellerId: data?.sellerId,
  });

  // Handle item updated events
  return {
    processed: true,
    eventId,
    eventDate,
    itemId: data?.itemId,
    sellerId: data?.sellerId,
    processedAt: new Date().toISOString(),
  };
}

async function processItemEnded(webhookData) {
  const { data, eventId, eventDate } = webhookData;

  console.log("Processing item ended:", {
    eventId,
    eventDate,
    itemId: data?.itemId,
    sellerId: data?.sellerId,
  });

  // Handle item ended events
  return {
    processed: true,
    eventId,
    eventDate,
    itemId: data?.itemId,
    sellerId: data?.sellerId,
    processedAt: new Date().toISOString(),
  };
}
