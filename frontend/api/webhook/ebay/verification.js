// eBay Webhook Verification Endpoint
// This endpoint handles eBay's webhook verification process

export default async function handler(req, res) {
  // Allow both GET and POST for verification
  if (req.method === "GET") {
    // Handle GET verification request
    const challengeCode = req.query.challenge_code;

    if (!challengeCode) {
      return res.status(400).json({
        error: "Missing challenge_code parameter",
        message: "eBay requires a challenge_code parameter for verification",
      });
    }

    console.log("eBay verification request received:", {
      challengeCode,
      timestamp: new Date().toISOString(),
    });

    // Return the challenge code as required by eBay
    return res.status(200).json({
      challengeResponse: challengeCode,
      timestamp: new Date().toISOString(),
    });
  }

  if (req.method === "POST") {
    // Handle POST verification request
    const { challengeCode } = req.body;

    if (!challengeCode) {
      return res.status(400).json({
        error: "Missing challengeCode in request body",
        message:
          "eBay requires a challengeCode in the request body for verification",
      });
    }

    console.log("eBay POST verification request received:", {
      challengeCode,
      timestamp: new Date().toISOString(),
    });

    // Return the challenge code as required by eBay
    return res.status(200).json({
      challengeResponse: challengeCode,
      timestamp: new Date().toISOString(),
    });
  }

  // Method not allowed
  return res.status(405).json({ error: "Method not allowed" });
}
