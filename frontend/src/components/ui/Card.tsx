import { motion } from 'framer-motion';
import { itemVariants, cardHover } from '../../lib/animations';
import styles from './Card.module.css';

interface CardProps {
    children: React.ReactNode;
    className?: string;
    glass?: boolean;
    hover?: boolean;
    glow?: boolean;
    gradient?: boolean;
    onClick?: () => void;
}

export function Card({
    children,
    className = '',
    glass = true,
    hover = false,
    glow = false,
    gradient = false,
    onClick,
}: CardProps) {
    const cardClasses = [
        styles.card,
        glass && styles.glass,
        glow && styles.glow,
        gradient && styles.gradient,
        onClick && styles.clickable,
        className,
    ]
        .filter(Boolean)
        .join(' ');

    return (
        <motion.div
            variants={itemVariants}
            whileHover={hover ? cardHover : undefined}
            className={cardClasses}
            onClick={onClick}
        >
            {children}
        </motion.div>
    );
}

interface CardHeaderProps {
    children: React.ReactNode;
    className?: string;
}

export function CardHeader({ children, className = '' }: CardHeaderProps) {
    return <div className={`${styles.header} ${className}`}>{children}</div>;
}

interface CardTitleProps {
    children: React.ReactNode;
    className?: string;
}

export function CardTitle({ children, className = '' }: CardTitleProps) {
    return <h3 className={`${styles.title} ${className}`}>{children}</h3>;
}

interface CardContentProps {
    children: React.ReactNode;
    className?: string;
}

export function CardContent({ children, className = '' }: CardContentProps) {
    return <div className={`${styles.content} ${className}`}>{children}</div>;
}

interface CardFooterProps {
    children: React.ReactNode;
    className?: string;
}

export function CardFooter({ children, className = '' }: CardFooterProps) {
    return <div className={`${styles.footer} ${className}`}>{children}</div>;
}
