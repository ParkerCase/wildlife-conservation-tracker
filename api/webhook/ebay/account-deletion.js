// eBay Account Deletion Webhook Endpoint
// Handles eBay marketplace account deletion/closure notifications and challenge verification

import { createHash } from "crypto";

const EBAY_VERIFICATION_TOKEN =
  "pvkK34ita66e1bGWe2Y3Gi6HDV4Hf4nXNQAlhIg46N2TWRJAto0KOvmAUxo370Nk";

export default async function handler(req, res) {
  if (req.method === "GET") {
    // eBay validation GET request
    const challengeCode = req.query.challenge_code;
    // Reconstruct the endpoint URL (must match what eBay is calling)
    const protocol = req.headers["x-forwarded-proto"] || "https";
    const host = req.headers["host"];
    const path = req.url.split("?")[0];
    const endpoint = `${protocol}://${host}${path}`;
    if (!challengeCode) {
      return res.status(400).json({ error: "Missing challenge_code" });
    }
    // Hash: challengeCode + verificationToken + endpoint
    const hash = createHash("sha256");
    hash.update(challengeCode);
    hash.update(EBAY_VERIFICATION_TOKEN);
    hash.update(endpoint);
    const responseHash = hash.digest("hex");
    return res.status(200).json({ challengeResponse: responseHash });
  }

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  // Strictly check the verification token
  const verificationToken =
    req.headers["x-ebay-verification-token"] || req.headers["x-ebay-signature"];
  if (!verificationToken || verificationToken !== EBAY_VERIFICATION_TOKEN) {
    return res
      .status(401)
      .json({ error: "Invalid or missing verification token" });
  }

  // eBay POST verification: respond to challenge (rare, but for completeness)
  if (req.body && req.body.challengeCode) {
    // Reconstruct the endpoint URL (must match what eBay is calling)
    const protocol = req.headers["x-forwarded-proto"] || "https";
    const host = req.headers["host"];
    const path = req.url.split("?")[0];
    const endpoint = `${protocol}://${host}${path}`;
    const hash = createHash("sha256");
    hash.update(req.body.challengeCode);
    hash.update(EBAY_VERIFICATION_TOKEN);
    hash.update(endpoint);
    const responseHash = hash.digest("hex");
    return res.status(200).json({ challengeResponse: responseHash });
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
  return {
    processed: true,
    eventId,
    eventDate,
    accountInfo: data?.accountInfo || {},
    deletionReason: data?.deletionReason || "Unknown",
    processedAt: new Date().toISOString(),
  };
}
