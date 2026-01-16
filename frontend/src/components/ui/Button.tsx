import { motion } from 'framer-motion';
import type { HTMLMotionProps } from 'framer-motion';
import { buttonTap } from '../../lib/animations';
import styles from './Button.module.css';

interface ButtonProps extends Omit<HTMLMotionProps<'button'>, 'children'> {
    variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
    size?: 'sm' | 'md' | 'lg';
    loading?: boolean;
    icon?: React.ReactNode;
    iconPosition?: 'left' | 'right';
    children?: React.ReactNode;
}

export function Button({
    children,
    variant = 'primary',
    size = 'md',
    loading = false,
    icon,
    iconPosition = 'left',
    disabled,
    className = '',
    ...props
}: ButtonProps) {
    const isDisabled = disabled || loading;

    return (
        <motion.button
            whileTap={isDisabled ? undefined : buttonTap}
            whileHover={isDisabled ? undefined : { scale: 1.02 }}
            className={`${styles.button} ${styles[variant]} ${styles[size]} ${className}`}
            disabled={isDisabled}
            {...props}
        >
            {loading ? (
                <span className={styles.spinner} />
            ) : (
                <>
                    {icon && iconPosition === 'left' && (
                        <span className={styles.icon}>{icon}</span>
                    )}
                    <span>{children}</span>
                    {icon && iconPosition === 'right' && (
                        <span className={styles.icon}>{icon}</span>
                    )}
                </>
            )}
        </motion.button>
    );
}
