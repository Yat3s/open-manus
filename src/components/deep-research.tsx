"use client";

import { useState, useRef } from "react";
import MarkdownPreviewer from "./markdown-previewer";
import { api } from "~/trpc/react";
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card";
import { Button } from "~/components/ui/button";
import { Loader2 } from "lucide-react";
import { Textarea } from "~/components/ui/textarea";
import html2pdf from "html-to-pdf-js";

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
  const researchContentRef = useRef<HTMLDivElement>(null);

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

  const handleDownloadPDF = async () => {
    if (!researchContentRef.current) return;

    try {
      const content = researchContentRef.current;
      const imgLinks = content.getElementsByTagName("img");
      const imgPromises = [];

      for (let i = 0; i < imgLinks.length; i++) {
        const img = imgLinks[i];
        if (!img) continue;

        const promise = new Promise<void>((resolve) => {
          const canvas = document.createElement("canvas");
          const ctx = canvas.getContext("2d");
          const image = new Image();

          image.crossOrigin = "anonymous";
          image.src = img.src || "";

          image.onload = () => {
            canvas.width = image.width;
            canvas.height = image.height;
            if (ctx) {
              ctx.drawImage(image, 0, 0);
              const base64 = canvas.toDataURL("image/png");
              img.src = base64;
              resolve();
            }
          };

          image.onerror = () => {
            console.error("Failed to load image:", img.src);
            resolve();
          };
        });

        imgPromises.push(promise);
      }

      await Promise.all(imgPromises);

      const element = researchContentRef.current;
      const opt = {
        margin: 10,
        filename: "research.pdf",
        image: { type: "jpeg", quality: 0.98 },
        html2canvas: {
          scale: 2,
          windowWidth: 1024,
          useCORS: true,
        },
        jsPDF: {
          unit: "mm",
          format: "a4",
          orientation: "portrait" as "portrait" | "landscape",
        },
        pagebreak: {
          mode: ["avoid-all"],
          before: ".page-break",
        },
      };

      await html2pdf().set(opt).from(element).save();
    } catch (error) {
      console.error("PDF generation failed:", error);
    }
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
            <CardContent className="space-y-8 p-8" ref={researchContentRef}>
              <div>
                <h2 className="mb-4 text-2xl font-semibold">
                  Research Summary
                </h2>
                <p>{research.summary}</p>
              </div>

              <div>
                <MarkdownPreviewer text={research.report} />
              </div>

              <div>
                <h2 className="mb-4 text-2xl font-semibold">
                  Follow-up Questions
                </h2>
                <ul className="list-disc space-y-2 pl-4">
                  {research.follow_up_questions.map((question, index) => (
                    <li key={index}>{question}</li>
                  ))}
                </ul>
              </div>
            </CardContent>
          </Card>

          <div className="flex justify-center">
            <Button onClick={handleDownloadPDF} variant="outline">
              Download PDF Report
            </Button>
          </div>
        </>
      )}
    </div>
  );
};

export default DeepResearch;
