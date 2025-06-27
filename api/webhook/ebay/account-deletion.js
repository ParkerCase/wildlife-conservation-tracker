// eBay Account Deletion Webhook Endpoint
// This endpoint handles eBay marketplace account deletion/closure notifications

export default async function handler(req, res) {
  // Only allow POST requests
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    // Log the incoming webhook for debugging
    console.log("eBay Account Deletion Webhook received:", {
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

    // Handle verification token validation
    const verificationToken =
      req.headers["x-ebay-signature"] ||
      req.headers["x-ebay-verification-token"];
    if (verificationToken) {
      console.log("Verification token received:", verificationToken);
      // You can add custom verification logic here if needed
      // For now, we'll just log it and accept it
    }

    // Process the account deletion notification
    const result = await processAccountDeletion(webhookData);

    // Return success response (eBay expects 200 status)
    return res.status(200).json({
      status: "success",
      message: "Account deletion notification processed successfully",
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

async function processAccountDeletion(webhookData) {
  // Extract relevant information from the webhook
  const {
    metadata,
    data,
    eventId,
    eventDate,
    publishDate,
    publishAttemptCount,
  } = webhookData;

  // Log the account deletion event
  console.log("Processing account deletion:", {
    eventId,
    eventDate,
    publishDate,
    publishAttemptCount,
    metadata,
    data,
  });

  // Here you can add your custom logic for handling account deletions
  // For example:
  // - Update your database to mark the account as deleted
  // - Stop monitoring this account
  // - Send notifications to your team
  // - Archive any relevant data

  // For now, we'll just return the processed data
  return {
    processed: true,
    eventId,
    eventDate,
    accountInfo: data?.accountInfo || {},
    deletionReason: data?.deletionReason || "Unknown",
    processedAt: new Date().toISOString(),
  };
}
