"use client";

import { useState } from "react";
import MarkdownPreviewer from "./markdown-previewer";
import { api } from "~/trpc/react";
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card";
import { Button } from "~/components/ui/button";
import { Loader2 } from "lucide-react";
import { Textarea } from "~/components/ui/textarea";

type Research = {
  trace_id: string;
  report: string;
  summary: string;
  follow_up_questions: string[];
};

const DeepResearch = () => {
  const [inputText, setInputText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [research, setResearch] = useState<Research | null>(null);

  const { mutateAsync: getResearch } = api.deepResearch.getResearch.useMutation(
    {
      onSettled: () => setIsLoading(false),
    },
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    const research = await getResearch({ prompt: inputText });
    setResearch(research);
  };

  return (
    <div className="mx-auto max-w-4xl space-y-6 px-4 py-8">
      <h1 className="text-center text-4xl font-bold">Deep Research</h1>

      <Card>
        <CardHeader>
          <CardTitle>Research Topic</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <Textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Enter your research topic..."
              className="min-h-[200px] w-full resize-none p-4"
            />
            <div className="flex justify-end">
              <Button
                disabled={isLoading}
                type="submit"
                className="w-fit"
                variant="default"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Generating...
                  </>
                ) : (
                  "Generate"
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {research && (
        <>
          <Card>
            <CardHeader>
              <CardTitle>Research Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <p>{research.summary}</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Detailed Report</CardTitle>
            </CardHeader>
            <CardContent>
              <MarkdownPreviewer text={research.report} />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Follow-up Questions</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="list-disc space-y-2 pl-4">
                {research.follow_up_questions.map((question, index) => (
                  <li key={index}>{question}</li>
                ))}
              </ul>
            </CardContent>
          </Card>

          <div className="text-center text-sm text-gray-500">
            Trace ID: {research.trace_id}
          </div>
        </>
      )}
    </div>
  );
};

export default DeepResearch;
