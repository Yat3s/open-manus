import { z } from "zod";
import axios from "axios";
import { createTRPCRouter, publicProcedure } from "~/server/api/trpc";

const REQUEST_TIMEOUT = 300000;

const ResearchResponse = z.object({
  trace_id: z.string(),
  report: z.string(),
  summary: z.string(),
  follow_up_questions: z.array(z.string()),
});

export const deepResearchRouter = createTRPCRouter({
  getResearch: publicProcedure
    .input(z.object({ prompt: z.string() }))
    .mutation(async ({ input }) => {
      return await deepResearch(input.prompt);
    }),
});

const deepResearch = async (prompt: string) => {
  try {
    const { data: research } = await axios.post<
      z.infer<typeof ResearchResponse>
    >(
      `${process.env.CORE_API_URL}/deep_research`,
      {
        query: prompt,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
        timeout: REQUEST_TIMEOUT,
      },
    );

    return research;
  } catch (error) {
    throw error;
  }
};
