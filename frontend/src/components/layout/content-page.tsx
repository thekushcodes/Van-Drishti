import { PublicLayout } from "./public-layout";
import { WildlifeCover } from "./wildlife-cover";
import type { ReactNode } from "react";
export function ContentPage({
  eyebrow,
  title,
  description,
  children,
}: {
  eyebrow: string;
  title: string;
  description: string;
  children: ReactNode;
}) {
  return (
    <PublicLayout>
      <section className="content-hero">
        <WildlifeCover />
        <div className="hero-shade" />
        <div>
          <div className="eyebrow">{eyebrow}</div>
          <h1>{title}</h1>
          <p>{description}</p>
        </div>
      </section>
      {children}
    </PublicLayout>
  );
}
