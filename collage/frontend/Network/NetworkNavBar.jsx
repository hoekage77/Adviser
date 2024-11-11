import React, { useState, lazy } from 'react';
import "../CSS/NetworkNavBar.css";
const Followers = lazy(() => import('./Followers'));
const Following = lazy(() => import('./Following'));
const Requests = lazy(() => import('./Requests'));
const Connect = lazy(() => import('./Connect'));

const NetworkNavBar = ({followerData, profileUser, handleViewProfile}) => {
  // State to track the active tab
  const [activeTab, setActiveTab] = useState('Connect');

  // Function to handle tab changes
  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  // Conditionally render based on the active tab
  const renderContent = () => {
    switch (activeTab) {
      case 'Connect':
        return <Connect currentUser={{id: 1}}/>;
        //can add the components here once they are completed
      case 'Requests':
        return <Requests currentUser={{id: 1}}/>;
      case 'Followers':
        return <Followers currentUser={{id: 1}}/>;
      case 'Following':
        return <Following currentUser={{id: 1}}/>;
      default:
        return null;
    }
  };

  return (
    <div className="network-navbar-wrapper">
      <nav className="network-navbar">
        <button
          className={`nav-button ${activeTab === 'Connect' ? 'red-highlight' : ''}`}
          onClick={() => handleTabChange('Connect')}
        >
          Connect
        </button>
        <button
          className={`nav-button ${activeTab === 'Requests' ? 'blue-highlight' : ''}`}
          onClick={() => handleTabChange('Requests')}
        >
          Requests
        </button>
        <button
          className={`nav-button ${activeTab === 'Followers' ? 'green-highlight' : ''}`}
          onClick={() => handleTabChange('Followers')}
        >
          Followers
        </button>
        <button
          className={`nav-button ${activeTab === 'Following' ? 'green-highlight' : ''}`}
          onClick={() => handleTabChange('Following')}
        >
          Following
        </button>
      </nav>

      <div className="content-area">
        {renderContent()}
      </div>
    </div>
  );
};

export default NetworkNavBar;
