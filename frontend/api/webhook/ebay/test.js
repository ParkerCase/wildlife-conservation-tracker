// Test endpoint for eBay webhook verification
// This can be used to test if the webhook is accessible and responding

export default async function handler(req, res) {
  // Allow both GET and POST for testing
  if (req.method === "GET") {
    return res.status(200).json({
      status: "success",
      message: "eBay webhook endpoint is accessible",
      timestamp: new Date().toISOString(),
      endpoint: "/api/webhook/ebay/test",
      availableEndpoints: [
        "/api/webhook/ebay/",
        "/api/webhook/ebay/account-deletion",
        "/api/webhook/ebay/test",
      ],
    });
  }

  if (req.method === "POST") {
    try {
      // Log the test request
      console.log("Test webhook received:", {
        timestamp: new Date().toISOString(),
        headers: req.headers,
        body: req.body,
      });

      // Return success response
      return res.status(200).json({
        status: "success",
        message: "Test webhook processed successfully",
        timestamp: new Date().toISOString(),
        receivedData: req.body,
        endpoint: "/api/webhook/ebay/test",
      });
    } catch (error) {
      console.error("Error processing test webhook:", error);

      return res.status(500).json({
        error: "Internal server error",
        message: error.message,
        timestamp: new Date().toISOString(),
      });
    }
  }

  // Method not allowed
  return res.status(405).json({ error: "Method not allowed" });
}
