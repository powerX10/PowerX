import { runBeamCommand } from "./providers/beam.js";

const TASK_ROUTES = {
  strategy_creation: "beam",
  financial_research: "beam",
  chart_analysis: "beam",
  technical_analysis: "cpu",
  trade_execution: "cpu",
  deep_research: "modal",
};

export async function executeTask(taskType, payload = {}) {
  const provider = TASK_ROUTES[taskType] || "modal";

  if (provider === "beam") {
    const command =
      payload.command ||
      `echo "PowerX task: ${taskType}"`;

    return await runBeamCommand({
      command,
      name: `powerx-${taskType}`,
    });
  }

  return {
    ok: true,
    provider,
    taskType,
    status: "provider_adapter_pending",
  };
}
