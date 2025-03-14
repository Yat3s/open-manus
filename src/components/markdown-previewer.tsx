/* eslint-disable */

import * as React from "react";
import { MemoizedReactMarkdown } from "~/components/markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import { CodeBlock } from "~/components/ui/codeblock";

const MarkdownPreviewer = ({ text }: { text: string }) => {
  return (
    <MemoizedReactMarkdown
      className="prose max-w-[calc(100vw_-_32px)] break-words dark:prose-invert prose-p:leading-relaxed prose-pre:p-0 sm:max-w-[56ch] md:max-w-2xl xl:max-w-[51rem]"
      remarkPlugins={[remarkGfm, remarkMath]}
      components={{
        p({ children }) {
          return <p className="mb-2 last:mb-0">{children}</p>;
        },
        a({ href, children, ...props }) {
          return (
            <a href={href} target="_blank" rel="noopener noreferrer" {...props}>
              {children}
            </a>
          );
        },
        code({ node, inline, className, children, ...props }) {
          if (children.length) {
            if (children[0] === "▍") {
              return (
                <span className="mt-1 animate-pulse cursor-default">▍</span>
              );
            }

            children[0] = (children[0] as string).replace("`▍`", "▍");
          }

          const match = /language-(\w+)/.exec(className || "");

          if (inline) {
            return (
              <code className={className} {...props}>
                {children}
              </code>
            );
          }

          return (
            <CodeBlock
              key={Math.random()}
              language={(match && match[1]) || ""}
              value={String(children).replace(/\n$/, "")}
              {...props}
            />
          );
        },
      }}
    >
      {text}
    </MemoizedReactMarkdown>
  );
};

export default MarkdownPreviewer;
