import wide from "@/assets/tiger-forest.jpg";

export function WildlifeCover({ priority = false }: { priority?: boolean }) {
  return (
    <picture>
      <img
        className="hero-photo"
        src={wide}
        width={2400}
        height={1250}
        alt="Photograph of a Bengal tiger in its forest habitat"
        fetchPriority={priority ? "high" : "auto"}
      />
    </picture>
  );
}

// import wide from "@/assets/tiger.jpeg";

// export function WildlifeCover({ priority = false }: { priority?: boolean }) {
//   return (
//     <picture>
//       <img
//         className="hero-photo"
//         src={wide}
//         width={2400}
//         height={1250}
//         alt="Tiger in its natural forest habitat"
//         fetchPriority={priority ? "high" : "auto"}
//       />
//     </picture>
//   );
// }
