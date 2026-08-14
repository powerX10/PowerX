import dotenv from "dotenv";
import { beamOpts, Sandbox, Image } from "@beamcloud/beam-js";

dotenv.config({ quiet: true });

beamOpts.token = process.env.BEAM_API_KEY;
beamOpts.workspaceId = process.env.BEAM_WORKSPACE_ID;

export async function runBeamCommand({
  command,
  cpu = 1,
  memory = 512,
  timeout = 120,
  name = "powerx-job",
}) {
  if (!beamOpts.token || !beamOpts.workspaceId) {
    throw new Error("Beam credentials are not configured.");
  }

  const image = new Image({
    baseImage: "ubuntu:22.04",
  });

  const sandbox = new Sandbox({
    name,
    image,
    cpu,
    memory,
    timeout,
  });

  let instance;

  try {
    instance = await sandbox.create();

    const result = await instance.exec([
      "sh",
      "-lc",
      command,
    ]);

    const exitCode = await result.wait();

    let stdout = "";
    let stderr = "";

    if (result.stdout) {
      for await (const chunk of result.stdout) {
        stdout += chunk;
      }
    }

    if (result.stderr) {
      for await (const chunk of result.stderr) {
        stderr += chunk;
      }
    }

    return {
      ok: exitCode === 0,
      provider: "beam",
      exitCode,
      stdout,
      stderr,
    };
  } finally {
    if (instance) {
      await instance.terminate();
    }
  }
}
