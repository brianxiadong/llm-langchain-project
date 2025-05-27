import React from 'react';
import './Navigation.css';

const Navigation = () => {
    return (
        <div className="navigation">
            <div className="segmented-control">
                <div className="segmented-control-container">
                    <div className="segment active">
                        <span>Tab</span>
                    </div>
                    <div className="segment">
                        <span>Tab</span>
                    </div>
                    <div className="segment">
                        <span>Tab</span>
                    </div>
                </div>
            </div>

            <div className="action-button">
                <button className="cta-button">
                    Call to action
                </button>
            </div>
        </div>
    );
};

export default Navigation; 